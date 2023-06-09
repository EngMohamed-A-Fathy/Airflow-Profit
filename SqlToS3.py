from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime 
from airflow.operators.python_operator import PythonOperator
from airflow.providers.amazon.aws.transfers.sql_to_s3 import SqlToS3Operator
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.operators.python_operator import BranchPythonOperator
import sys

sys.path.append('/opt/airflow/includes')
from emp_dim_insert_update import join_and_detect_new_or_changed_rows
from queries import *

def check_rows_to_update(**kwargs):
    rows_to_update = kwargs['ti'].xcom_pull(task_ids="join_and_detect_new_or_changed_rows", key="ids_to_update")
    if not rows_to_update:
        return "insert_task_to_snowflake"
    else:
        return "update_task_to_snowflake"


with DAG("SqlToS3", start_date=datetime(2023, 5, 14), schedule_interval='@hourly', catchup=False) as dag:

    sql_to_s3_task1 = SqlToS3Operator(
        task_id='transfer_sql_to_s3_1',
        query= "SELECT * FROM finance.emp_sal",
        s3_bucket='staging.emp.data',
        s3_key='fathy_emp_sal.csv',
        sql_conn_id='ConnToPost',
        aws_conn_id='ConnToAWS',
        replace=True 
    )
    
    sql_to_s3_task2 = SqlToS3Operator(
        task_id='transfer_sql_to_s3_2',
        query= "SELECT * FROM hr.emp_details",
        s3_bucket='staging.emp.data',
        s3_key='fathy_emp_details.csv',
        sql_conn_id='ConnToPost',
        aws_conn_id='ConnToAWS',
        replace=True  
    )
    
    transform_task3 = join_and_detect_new_or_changed_rows()
    
    check_rows_task = BranchPythonOperator(
            task_id='check_rows_to_update',
            python_callable=check_rows_to_update
        )    
        
    update_task_to_snowflake = SnowflakeOperator(
        task_id='update_task_to_snowflake',
        sql=UPDATE_DWH_EMP_DIM('{{ ti.xcom_pull(task_ids="join_and_detect_new_or_changed_rows", key = "ids_to_update")}}'),
        schema = 'dimension',
        snowflake_conn_id='snowConn'
    )

    insert_task_to_snowflake = SnowflakeOperator(
        task_id="insert_task_to_snowflake",
        sql=INSERT_INTO_DWH_EMP_DIM('{{ ti.xcom_pull(task_ids="join_and_detect_new_or_changed_rows", key = "rows_to_insert")}}'),
        schema = 'dimension',
        snowflake_conn_id='snowConn'
    )
    
    insert_task_to_snowflake2 = SnowflakeOperator(
        task_id="insert_task_to_snowflake2",
        sql=INSERT_INTO_DWH_EMP_DIM('{{ ti.xcom_pull(task_ids="join_and_detect_new_or_changed_rows", key = "rows_to_insert")}}'),
        schema = 'dimension',
        snowflake_conn_id='snowConn'
    )
    check_rows_task >> update_task_to_snowflake >> insert_task_to_snowflake2
    check_rows_task >> insert_task_to_snowflake
    sql_to_s3_task1 >> sql_to_s3_task2 >> transform_task3 >> check_rows_task
    


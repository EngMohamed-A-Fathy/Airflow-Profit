# Airflow Data Pipeline: Load Employee Data from S3 to Snowflake
This project demonstrates an Apache Airflow data pipeline for loading employee data from an S3 bucket to Snowflake. The pipeline automates the process of extracting data from PostgreSQL, uploading it to S3, joining and detecting new or changed rows, and finally loading the data into Snowflake.

The project is designed for a company that updates its employees' salary once per year. The data pipeline handles this scenario by detecting new inserted rows with updated salary information. If an employee already exists in the database, the pipeline updates the existing row with the current date and inserts a new row with the updated salary and a high date. If an employee doesn't exist in the database, the pipeline simply inserts a new row.

By implementing this pipeline, the company can efficiently manage its employee data and ensure that the latest salary information is accurately recorded in Snowflake.

## Prerequisites
### Before running the pipeline, ensure that the following requirements are met:

Apache Airflow is installed. You can refer to the Airflow documentation for installation instructions.
Access to a PostgreSQL database with the required tables (finance.emp_sal and hr.emp_details), and a Snowflake database for loading the data.
Proper configuration of connections in Airflow:
postgres_connection: PostgreSQL connection details for reading data from the database.
aws_connection: AWS S3 connection details for uploading data to S3.
snowflake_conn: Snowflake connection details for loading data into Snowflake.
## Project Structure
### The project structure is organized as follows:

dags/: Directory containing the Airflow DAG definition file.
includes/: Directory containing custom Python modules used in the DAG.
queries/: Directory containing SQL queries used in the DAG.

## Project Structure

### DAG Description
The DAG (LoadEmpDataFromS3ToSnowflake) consists of the following tasks:

![1](https://github.com/EngMohamed-A-Fathy/Airflow-Profit/assets/128105398/bf524814-9c32-438d-bd91-5860be629847)

transfer_sql_to_s3_1: Reads data from the finance.emp_sal table in PostgreSQL and uploads it to the specified S3 bucket.
transfer_sql_to_s3_2: Reads data from the hr.emp_details table in PostgreSQL and uploads it to the specified S3 bucket.
join_and_detect_new_or_changed_rows: Executes a custom Python function to join the data and detect new or changed rows.
check_rows_to_update: Branches the workflow based on the presence of new or changed rows.
insert_task_to_snowflow: Inserts new rows into the DWH_EMP_DIM table in Snowflake.
update_task_to_snowflow: Updates changed rows in the DWH_EMP_DIM table in Snowflake.
insert_task_to_snowflow_2: Inserts new rows into the DWH_EMP_DIM table in Snowflake.

## Usage
To use this project, follow these steps:

Set up Apache Airflow and ensure all required connections are configured properly.
Copy the DAG file load_emp_data.py from the dags/ directory to your Airflow DAGs folder.
Place the custom Python module emp_dim_insert_update.py inside the includes/ directory.
Create a queries/ directory and populate it with the necessary SQL query files (INSERT_INTO_DWH_EMP_DIM.sql and UPDATE_DWH_EMP_DIM.sql).
Update the DAG file and connection details according to your environment.

### Please note that this README assumes familiarity with Apache Airflow and the necessary configurations for PostgreSQL, S3, and Snowflake connections.

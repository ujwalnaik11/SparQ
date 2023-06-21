from datetime import timedelta, datetime
import os
import requests
from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator 
from airflow.providers.apache.spark.operators.spark_jdbc import SparkJDBCOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python import PythonOperator
from airflow.models import Variable


dag_spark = DAG(
        dag_id = "sparkSubmit_local",
        #default_args=args,
        schedule_interval='@once',	
        dagrun_timeout=timedelta(minutes=60),
        description='use case of sparkoperator in airflow',
        start_date=datetime(2022, 12, 15), catchup=False
)

def custom_get_contents_then_save():
    data_path = f"/opt/airflow/dags/app/superset.csv"

    os.makedirs(os.path.dirname(data_path), exist_ok=True)

    url = "https://raw.githubusercontent.com/ujwalnaik11/dataset-files/master/superset.csv"

    response = requests.request("GET", url)

    with open(data_path, "w") as file:
        file.write(response.text)

save_csv = PythonOperator(task_id='fetch_csv', python_callable=custom_get_contents_then_save, dag=dag_spark)


spark_submit = SparkSubmitOperator(
		conn_id= 'spark_default', 
		task_id='spark_submit', 
        application= f"/opt/airflow/dags/app/spark-app.py",
        #total_executor_cores=2,
        executor_cores=2,
        jars = f"/opt/airflow/dags/app/postgresql-42.5.1.jar", 
        packages= "io.delta:delta-core_2.12:2.2.0",
        executor_memory='512m',
        driver_memory='512m',
		dag=dag_spark
		)


create_postgres_table = PostgresOperator(
        postgres_conn_id= 'airflow_postgres', 
		task_id='create_table', 
        dag=dag_spark, 
        sql = """ CREATE TABLE IF NOT EXISTS dag_runs (
    id INT PRIMARY KEY ,
    FL_DATE DATE,
    OP_CARRIER VARCHAR(20),
    OP_CARRIER_FL_NUM INT,
    ORIGIN_CITY_NAME VARCHAR(50),
    DEST_CITY_NAME VARCHAR(50),
    CRS_DEP_TIME INT,
    DEP_TIME INT,
    WHEELS_ON INT,TAXI_IN INT, CRS_ARR_TIME INT, ARR_TIME INT, CANCELLED INT, DISTANCE INT 
)
        """
       
)


save_csv >> create_postgres_table >> spark_submit 

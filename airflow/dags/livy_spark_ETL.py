import os
from datetime import datetime

from airflow import DAG
from airflow.providers.apache.livy.operators.livy import LivyOperator

DAG_ID = "livy_operator"

dag = DAG(
    dag_id=DAG_ID,
    schedule="@daily",
    start_date=datetime(2021, 1, 1),
    catchup=False,
) 

livy_python_task = LivyOperator(
        task_id= "spark_task", 
        file= f"/opt/airflow/dags/app/spark-app.py", 
        polling_interval= 10, 
        livy_conn_id = "livy_default" ,
        executor_cores= 2,
        executor_memory='512m',
        driver_memory='512m',
        jars = f"/opt/airflow/dags/app/postgresql-42.5.1.jar"
        )

livy_python_task
    
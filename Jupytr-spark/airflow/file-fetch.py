import os
from datetime import datetime
import requests
from airflow import DAG
from airflow.decorators import task
import logging

from airflow.operators.python import PythonOperator

with DAG('fileFetch', description='fetchCSV',
          schedule_interval='0 */2 * * *',
          start_date=datetime(2022, 12, 14), catchup=False) as dag:


    @task
    def custom_get_contents_then_save_task():
        data_path = f"/opt/bitnami/airflow/dags/data{datetime.now()}.csv"
        logging.info('Write Dir')
        os.makedirs(os.path.dirname(data_path), exist_ok=True)
        logging.info(f'File={data_path}')

        url = "https://raw.githubusercontent.com/apache/airflow/main/docs/apache-airflow/pipeline_example.csv"

        response = requests.request("GET", url)

        with open(data_path, "w") as file:
            file.write(response.text)

        logging.info(f'Data written to File={data_path}')


   

    custom_get_contents_then_save_task()

from airflow import DAG
from airflow.providers.papermill import PapermillOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime

dag = DAG(
    dag_id="example_papermill_operator_verify",
    schedule='0 */2 * * *',
    start_date=datetime(2022, 12, 15),
    catchup=False,
)

run_this = PapermillOperator(
        task_id="run_example_notebook",
        input_nb="/tmp/airflow.ipynb",
        output_nb="/tmp/out-{{ execution_date }}.ipynb",
        parameters={"msgs": "Ran from Airflow at {{ execution_date }}!"},
        dag= dag
    )

dummy_operator = DummyOperator(task_id='dummy_task', retries=3, dag=dag)

dummy_operator >> run_this




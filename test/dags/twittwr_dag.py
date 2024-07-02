from airflow.decorators import task,dag
from datetime import timedelta,datetime

default_args={
    'owner': 'tien',
    'retries':5,
    'retry_delay':timedelta(minutes=5)
}

@dag(
    dag_id='twitter_dag',
    default_args=default_args,
    description='My first ETL code'
)

def twitter_pipeline():
    @task()
    def run_etl():
        


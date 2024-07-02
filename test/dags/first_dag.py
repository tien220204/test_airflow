
from airflow import DAG
from datetime import datetime,timedelta
from airflow.operators.bash import BashOperator



default_args ={
    'owner': 'tien',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG (
    dag_id='first_dag',
    description='initial dag description',
    default_args=default_args,
    start_date=datetime(2021, 7, 29, 2),
    schedule_interval = '@daily'
) as dag:
    task1 = BashOperator(
        task_id='task1',
        bash_command='echo Hello World'
        )
    
    task2 = BashOperator(
        task_id='task2',
        bash_command='echo task2'
    )
    
task1.set_downstream(task2)
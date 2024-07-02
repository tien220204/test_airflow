from airflow.decorators import task,dag
from datetime import timedelta,datetime

default_args={
    'owner': 'tien',
    'retries':5,
    'retry_delay':timedelta(minutes=5)
}

@dag(
    dag_id='taskflow_api_dag',
    default_args=default_args,
    start_date=datetime(2024,6,23,5),
    schedule_interval='@daily'
)
def hello():
    @task(multiple_outputs=True)
    def get_name():
        return {
            'first_name': 'John',
            'last_name': 'Arin'
        }
    @task()
    def get_age():
        return 19
    @task()
    def greet(first_name, last_name, age):
        print(f'Hello {first_name} {last_name}, age: {age}')
    full_name = get_name()
    first_name = full_name['first_name']
    last_name = full_name['last_name']
    age = get_age()
    greet(first_name=first_name,last_name=last_name, age = age)
taskflow_api_dag = hello()
from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
# du lieu xcom chi toi da 48kb
default_args = {
    'owner': 'tien',
    'retries': 5,
    'retry_delay': timedelta(minutes=2),
}

def greet(ti):
    first_name = ti.xcom_pull(task_ids='get_name',key='first_name')
    last_name = ti.xcom_pull(task_ids='get_name',key='last_name')
    age = ti.xcom_pull(task_ids='get_age',key='age')
    print(f'Hello {first_name} {last_name}, age: {age}')
def get_name(ti):
    ti.xcom_push(key='first_name',value='John')
    ti.xcom_push(key='last_name',value='Arin')
def get_age(ti):
    ti.xcom_push(key='age',value='24')
with DAG(
    dag_id="python_operators_dag",
    description='abc',
    default_args=default_args,
    start_date=datetime(2024,6,22,10),
    schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
       task_id="greet",
       python_callable=greet,
    #    op_kwargs={ 'age':24}
    )
    task2 = PythonOperator(
        task_id="get_name",
        python_callable=get_name,
        
    )
    task3 = PythonOperator(
        task_id='get_age',
        python_callable=get_age
    )

[task2,task3]>>task1
    
    
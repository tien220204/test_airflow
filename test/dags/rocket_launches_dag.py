import json
from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import pathlib
import requests
from requests.exceptions import MissingSchema

default_args = {
    'owner': 'rocket_launches_dag',
    'retries':5,
    'retry_delay': timedelta(minutes=5)
}
def _get_pictures():
    pathlib.Path("/tmp/images").mkdir(parents=True, exist_ok=True)
    # Download all pictures in launches.json
    with open("/tmp/launches.json") as f:
        launches = json.load(f)
        image_urls = [launch["image"] for launch in launches["results"]]
        for image_url in image_urls:
            try:
                response = requests.get(image_url)
                image_filename = image_url.split("/")[-1]
                target_file = f"/tmp/images/{image_filename}" 
                with open(target_file,"wb") as f:
                    f.write(response.content)
                print(f'Downloaded {image_url} to {target_file}')
            except MissingSchema as e:
                print(f'{image_url} appears to be invalid URL.')

with DAG(
    dag_id = 'rocket_launches_dag',
    default_args = default_args,
    start_date = datetime(2024,6,25),
    schedule_interval = None
) as dag:
    download_lauches = BashOperator(
        task_id = 'download_lauches',
        bash_command='curl -o /tmp/launches.json -L "https://ll.thespacedevs.com/2.0.0/launch/upcoming"'
    )
    get_pictures = PythonOperator(
        task_id = 'get_pictures',
        python_callable=_get_pictures
    )
    notify = BashOperator(
        task_id = 'notify',
        bash_command='echo "There are now $(ls /tmp/images/ | wc -l) images."'
    )
download_lauches >> get_pictures >> notify
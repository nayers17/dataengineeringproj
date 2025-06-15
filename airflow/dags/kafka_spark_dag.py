from airflow import DAG
from airflow.operators.bash import BashOperator # type: ignore
from datetime import datetime, timedelta

default_args = {
    'owner': 'you',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='kafka_to_spark',
    default_args=default_args,
    start_date=datetime(2025, 6, 15),
    schedule='@hourly',
    catchup=False
) as dag:
    
    produce = BashOperator(
        task_id='produce_messages',
        bash_command='python /producer/producer.py'
    )
    
    spark_job = BashOperator(
        task_id="run_spark_stream",
        bash_command=(
            # jump into the running Spark-master container
            "docker exec apache-data-eng-spark-master-1 "
            # give it a full path just to be safe
            "/opt/bitnami/spark/bin/spark-submit "
            "--master spark://spark-master:7077 "
            "--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 "
            "/opt/bitnami/spark/jobs/stream_processor.py"
        ),
    )
    
    consume = BashOperator(
        task_id='verify_consume',
        bash_command='docker exec kafka python /consumer/consumer.py'
    )
    

    
    produce >> spark_job >> consume
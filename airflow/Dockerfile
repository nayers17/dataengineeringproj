# airflow/Dockerfile
FROM apache/airflow:2.5.3

USER root
RUN apt-get update -qq \
 && apt-get install -y -qq docker.io \
 && rm -rf /var/lib/apt/lists/*

# switch back to the airflow user before doing Python installs
USER airflow

# copy & install your producer requirements into --user site
COPY producer/requirements.txt /requirements/producer.txt
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir --user -r /requirements/producer.txt

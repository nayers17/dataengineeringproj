# Apache Data Engineering Playground

A local Docker-based sandbox to practice core Apache data-engineering tools (Kafka KRaft, Spark, Airflow) without any cloud dependencies.

---

## Contents

1. [Prerequisites](#prerequisites)  
2. [Services & Ports](#services--ports)  
3. [Getting Started](#getting-started)  
4. [One-Time Initialization](#one-time-initialization)  
5. [Daily Workflows](#daily-workflows)  
6. [Project Layout](#project-layout)  
7. [Tips & Troubleshooting](#tips--troubleshooting)  

---

## Prerequisites

- Docker & Docker Compose  
- Python 3.8+ (for local scripts)  
- (Optional) VS Code or your favorite editor  

---

## Services & Ports

| Service          | Image                   | Ports           | Notes                         |
|------------------|-------------------------|-----------------|-------------------------------|
| **Kafka (KRaft)**    | `bitnami/kafka:3.4`       | `9092`, `9093`  | Broker + controller mode      |
| **Spark Master** | `bitnami/spark:3.3`     | `7077`, `8080`  | Spark standalone cluster      |
| **Spark Worker** | `bitnami/spark:3.3`     | _internal_      | Joins master at `7077`        |
| **Postgres**     | `postgres:13`           | `5432`          | Airflow metadata DB (persisted in volume) |
| **Airflow Web**  | `apache/airflow:2.5.3`  | `8081 → 8080`   | UI & REST API                 |
| **Airflow Sched**| `apache/airflow:2.5.3`  | _no host port_  | Scheduler                     |

---

## Getting Started

1. **Clone this repo**  
   ```bash
   git clone https://github.com/nayers17/dataengineeringproj.git
   cd dataengineeringproj
Bring up only Postgres (to prepare the volume):

bash
Copy
Edit
docker-compose up -d airflow-postgres
One-Time Initialization
You only ever do this once (per fresh volume).

Initialize Airflow’s metadata database

bash
Copy
Edit
docker-compose run --rm airflow-web airflow db init
Create an Admin user

bash
Copy
Edit
docker-compose run --rm airflow-web airflow users create \
  --username admin \
  --firstname Admin --lastname User \
  --role Admin \
  --email admin@example.org \
  --password admin
‣ Login: admin / admin

Daily Workflows
Bring up all core services

bash
Copy
Edit
docker-compose up -d \
  kafka spark-master spark-worker \
  airflow-web airflow-scheduler
Verify

bash
Copy
Edit
docker-compose ps
All containers should be Up and Airflow-web should show 0.0.0.0:8081->8080.

Access UIs

Airflow: http://localhost:8081

Spark: http://localhost:8080

Stopping everything

bash
Copy
Edit
docker-compose down
(Vol­umes are preserved, so your Postgres & Kafka data survive.)

Project Layout
bash
Copy
Edit
├─ airflow/
│   ├─ dags/          ← your DAG files
│   ├─ logs/          ← Airflow task logs (bind-mounted)
│   └─ plugins/       ← custom operators/hooks
│
├─ producer/
│   └─ producer.py    ← Python Kafka producer
│
├─ consumer/
│   └─ consumer.py    ← Python Kafka consumer
│
├─ spark/
│   └─ jobs/
│       └─ stream_processor.py  ← PySpark job reading from Kafka
│
├─ docker-compose.yml
└─ README.md
Tips & Troubleshooting
.yml changes → always docker-compose down then docker-compose up -d.

Airflow DB errors (“need to initialize”) mean you skipped step 3.

Permission denied on logs → ensure your local airflow/logs folder exists and is writable by your user.

Kafka connectivity in Spark/Airflow containers: point to kafka:9092 (not localhost), since they share the Docker network.

Inspect logs with docker-compose logs -f <service> or tail only errors docker-compose logs kafka 2>&1 | grep ERROR.

Now you have a reproducible, version-controlled environment to:

produce messages into Kafka

run a Spark streaming job on them

orchestrate everything via Airflow

Feel free to expand with more services (e.g. Airflow > XCom, HDFS, Elasticsearch) as you go!

# Airflow + dbt integration using Astronomer Cosmos

This project gives you an example of integrating [dbt (Data build tool)](https://docs.getdbt.com) with [Apache Airflow](https://airflow.apache.org/) using [Astronomer Cosmos](https://astronomer.github.io/astronomer-cosmos/index.html).

- Run your dbt Core projects as Apache Airflow® DAGs and Task Groups with a few lines of code. Benefits include:
- Run dbt projects against Airflow connections instead of dbt profiles
- Native support for installing and running dbt in a virtual environment to avoid dependency conflicts with Airflow
- Run tests immediately after a model is done to catch issues early
- Utilize Airflow’s data-aware scheduling to run models immediately after upstream ingestion
- Turn each dbt model into a task/task group complete with retries, alerting, etc.

## Requirements

- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Docker Compose: [Install Docker Compose](https://docs.docker.com/compose/install/)

## Preparations

1. Clone repo:

   ```bash
   git clone git@github.com:Simarglok/airflow_cosmos_demo.git
   cd airflow_cosmos_demo
   ```

2. Update `.env` if you need:

## Running Airflow

To run project using Docker Compose, execute following commands:

1. Build containers:

   ```bash
   docker-compose build
   ```

2. Run the containers in the background:

   ```bash
   docker-compose up -d
   ```

3. To view logs:

   ```bash
   docker-compose logs -f
   ```

4. Stopping the containers:

   ```bash
   docker-compose stop
   ```

## Useful commands

- Restart containers:

  ```bash
  docker-compose restart
  ```

- Connect to conteiner:

  ```bash
  docker exec -it container_name /bin/bash
  ```

- Remove all containers and networks:

  ```bash
  docker-compose down --volumes --remove-orphans
  ```

## Running DAG's

- First unpause **dbt_docs_generator** DAG to generate dbt documentation including manifest.json file

- Second unpause **dbt_simple_task_group** DAG to run dbt project

- Also you can try **dbt_simple_bash** to see how it works in old way with BashOperator

## dbt documentation

dbt Docs will be available in Airflow UI menu: 
   - [Browse -> dbt Docs](http://localhost:8080/cosmos/dbt_docs)

## Project structure

```
airflow_cosmos_demo/
├── docker-compose.yml           # Docker Compose configuration
├── .env                         # Environment variables
├── dags/                        # Airflow DAG's with Cosmos
├── dbt/                         # Jaffle Shop dbt project
├── Dockerfile                   # Docker file based on apache/airflow:2.9.2-python3.12 image
├── requirements.txt             # Additional requirements for Airflow
├── requirements_dbt_venv.txt    # Requirements for dbt's virtual environment
└── README.md                    # Project documentstion
```

## License

Apache 2.0

---

### Author

- [**Simarglok**](https://github.com/Simarglok)

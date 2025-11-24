---
name: "Data Pipeline"
description: "You are an expert at building robust data pipelines and ETL processes."
---

# Data Pipeline

You are an expert at building robust data pipelines and ETL processes.

## Activation

This skill activates when the user needs help with:
- Building ETL/ELT pipelines
- Data orchestration (Airflow, Prefect)
- Streaming data processing
- Batch data processing
- Data warehouse loading

## Process

### 1. Pipeline Assessment
Ask about:
- Data sources and destinations
- Volume and velocity
- Processing frequency (batch/streaming)
- Data quality requirements
- Infrastructure constraints

### 2. Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    DATA PIPELINE ARCHITECTURE                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  SOURCES           INGESTION        TRANSFORM        SERVE      │
│  ┌─────┐          ┌─────────┐      ┌─────────┐     ┌─────────┐ │
│  │ API │─────────▶│  Raw    │─────▶│ Cleaned │────▶│  Data   │ │
│  └─────┘          │  Layer  │      │  Layer  │     │  Mart   │ │
│  ┌─────┐          └─────────┘      └─────────┘     └─────────┘ │
│  │ DB  │─────────▶     │                │               │       │
│  └─────┘               │                │               │       │
│  ┌─────┐               ▼                ▼               ▼       │
│  │Files│─────────▶┌─────────┐      ┌─────────┐     ┌─────────┐ │
│  └─────┘          │  Data   │      │  dbt    │     │   BI    │ │
│                   │  Lake   │      │ Models  │     │  Tools  │ │
│                   └─────────┘      └─────────┘     └─────────┘ │
│                                                                  │
│  ──────────────────────────────────────────────────────────────  │
│  │           Orchestration (Airflow/Prefect)                 │  │
│  ──────────────────────────────────────────────────────────────  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 3. Apache Airflow DAG

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator
from airflow.utils.task_group import TaskGroup

default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'email': ['data@company.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'retry_exponential_backoff': True,
}

with DAG(
    dag_id='daily_sales_pipeline',
    default_args=default_args,
    description='Daily sales data pipeline',
    schedule_interval='0 6 * * *',  # Daily at 6 AM
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['sales', 'daily'],
    max_active_runs=1,
) as dag:

    start = EmptyOperator(task_id='start')

    # Extract tasks
    with TaskGroup(group_id='extract') as extract_group:

        def extract_api_data(**context):
            """Extract data from API."""
            import requests
            import json

            execution_date = context['ds']
            response = requests.get(
                f"https://api.example.com/sales?date={execution_date}",
                headers={"Authorization": f"Bearer {Variable.get('api_token')}"}
            )
            data = response.json()

            # Save to S3
            s3_hook = S3Hook(aws_conn_id='aws_default')
            s3_hook.load_string(
                string_data=json.dumps(data),
                key=f"raw/sales/{execution_date}/api_data.json",
                bucket_name='data-lake-bucket'
            )
            return len(data)

        extract_api = PythonOperator(
            task_id='extract_api',
            python_callable=extract_api_data,
        )

        extract_db = PostgresOperator(
            task_id='extract_orders',
            postgres_conn_id='source_db',
            sql="""
                COPY (
                    SELECT * FROM orders
                    WHERE created_at::date = '{{ ds }}'
                )
                TO STDOUT WITH CSV HEADER;
            """,
        )

    # Transform tasks
    with TaskGroup(group_id='transform') as transform_group:

        def clean_and_transform(**context):
            """Clean and transform data."""
            import pandas as pd
            from io import StringIO

            execution_date = context['ds']

            # Read from S3
            s3_hook = S3Hook(aws_conn_id='aws_default')
            raw_data = s3_hook.read_key(
                key=f"raw/sales/{execution_date}/api_data.json",
                bucket_name='data-lake-bucket'
            )

            df = pd.read_json(StringIO(raw_data))

            # Clean data
            df = df.dropna(subset=['order_id', 'amount'])
            df['amount'] = df['amount'].astype(float)
            df['created_at'] = pd.to_datetime(df['created_at'])

            # Transform
            df['date'] = df['created_at'].dt.date
            df['hour'] = df['created_at'].dt.hour

            # Save processed data
            s3_hook.load_string(
                string_data=df.to_parquet(index=False),
                key=f"processed/sales/{execution_date}/sales.parquet",
                bucket_name='data-lake-bucket'
            )

        transform = PythonOperator(
            task_id='transform_data',
            python_callable=clean_and_transform,
        )

    # Load tasks
    with TaskGroup(group_id='load') as load_group:

        load_to_warehouse = S3ToRedshiftOperator(
            task_id='load_to_redshift',
            schema='analytics',
            table='sales',
            s3_bucket='data-lake-bucket',
            s3_key='processed/sales/{{ ds }}/sales.parquet',
            redshift_conn_id='redshift_default',
            aws_conn_id='aws_default',
            copy_options=['FORMAT AS PARQUET'],
            method='UPSERT',
            upsert_keys=['order_id'],
        )

    # Quality checks
    def run_quality_checks(**context):
        """Run data quality checks."""
        from great_expectations import get_context

        context = get_context()
        checkpoint_result = context.run_checkpoint(
            checkpoint_name="sales_checkpoint",
            batch_request={
                "datasource_name": "redshift",
                "data_asset_name": "sales",
            }
        )

        if not checkpoint_result.success:
            raise Exception("Data quality checks failed!")

    quality_check = PythonOperator(
        task_id='quality_check',
        python_callable=run_quality_checks,
    )

    end = EmptyOperator(task_id='end')

    # Define dependencies
    start >> extract_group >> transform_group >> load_group >> quality_check >> end
```

### 4. Prefect Flow

```python
from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta
import pandas as pd

@task(
    retries=3,
    retry_delay_seconds=60,
    cache_key_fn=task_input_hash,
    cache_expiration=timedelta(hours=1)
)
def extract_data(source_url: str, date: str) -> pd.DataFrame:
    """Extract data from source."""
    import requests

    response = requests.get(f"{source_url}?date={date}")
    return pd.DataFrame(response.json())

@task
def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and transform data."""
    # Remove nulls
    df = df.dropna(subset=['id', 'value'])

    # Type conversions
    df['value'] = df['value'].astype(float)
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Add derived columns
    df['date'] = df['timestamp'].dt.date
    df['is_high_value'] = df['value'] > 1000

    return df

@task
def load_data(df: pd.DataFrame, table_name: str):
    """Load data to warehouse."""
    from sqlalchemy import create_engine

    engine = create_engine(os.getenv('WAREHOUSE_URL'))
    df.to_sql(
        table_name,
        engine,
        if_exists='append',
        index=False,
        method='multi'
    )

@task
def validate_data(table_name: str, date: str) -> bool:
    """Validate loaded data."""
    from sqlalchemy import create_engine, text

    engine = create_engine(os.getenv('WAREHOUSE_URL'))
    with engine.connect() as conn:
        result = conn.execute(text(f"""
            SELECT COUNT(*) as cnt
            FROM {table_name}
            WHERE date = '{date}'
        """))
        count = result.scalar()

    if count == 0:
        raise ValueError(f"No data loaded for {date}")

    return True

@flow(name="daily-sales-pipeline")
def sales_pipeline(date: str = None):
    """Daily sales data pipeline."""
    from datetime import datetime

    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')

    # Extract
    raw_data = extract_data(
        source_url="https://api.example.com/sales",
        date=date
    )

    # Transform
    clean_data = transform_data(raw_data)

    # Load
    load_data(clean_data, table_name="sales")

    # Validate
    validate_data(table_name="sales", date=date)

if __name__ == "__main__":
    sales_pipeline()
```

### 5. Streaming Pipeline (Kafka + Flink)

```python
# Kafka consumer with processing
from kafka import KafkaConsumer, KafkaProducer
import json

def process_stream():
    consumer = KafkaConsumer(
        'raw-events',
        bootstrap_servers=['kafka:9092'],
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        group_id='event-processor',
        auto_offset_reset='earliest'
    )

    producer = KafkaProducer(
        bootstrap_servers=['kafka:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    for message in consumer:
        event = message.value

        # Transform
        processed = {
            'event_id': event['id'],
            'event_type': event['type'],
            'user_id': event.get('user_id'),
            'timestamp': event['timestamp'],
            'processed_at': datetime.utcnow().isoformat()
        }

        # Enrich
        if event['type'] == 'purchase':
            processed['amount'] = float(event['data']['amount'])

        # Send to processed topic
        producer.send('processed-events', value=processed)
        producer.flush()
```

### 6. dbt Model

```sql
-- models/staging/stg_sales.sql
{{ config(materialized='view') }}

SELECT
    id AS sale_id,
    customer_id,
    product_id,
    CAST(amount AS DECIMAL(10,2)) AS amount,
    CAST(quantity AS INTEGER) AS quantity,
    CAST(created_at AS TIMESTAMP) AS created_at,
    DATE(created_at) AS sale_date
FROM {{ source('raw', 'sales') }}
WHERE amount IS NOT NULL
  AND amount > 0

-- models/marts/fct_daily_sales.sql
{{ config(
    materialized='incremental',
    unique_key='sale_date'
) }}

SELECT
    sale_date,
    COUNT(DISTINCT sale_id) AS total_orders,
    COUNT(DISTINCT customer_id) AS unique_customers,
    SUM(amount) AS total_revenue,
    AVG(amount) AS avg_order_value
FROM {{ ref('stg_sales') }}
{% if is_incremental() %}
WHERE sale_date > (SELECT MAX(sale_date) FROM {{ this }})
{% endif %}
GROUP BY sale_date
```

## Output Format

Provide:
1. Pipeline architecture diagram
2. DAG/Flow code
3. Data transformation logic
4. Quality checks
5. Deployment instructions

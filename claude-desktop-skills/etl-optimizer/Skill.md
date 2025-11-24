---
name: "ETL Optimizer"
description: "You are an expert at optimizing ETL/ELT pipelines for performance and efficiency."
version: "1.0.0"
---

# ETL Optimizer

You are an expert at optimizing ETL/ELT pipelines for performance and efficiency.

## Activation

This skill activates when the user needs help with:
- ETL performance optimization
- Query optimization for data pipelines
- Parallel processing strategies
- Memory management
- Pipeline bottleneck resolution

## Process

### 1. Optimization Assessment
Ask about:
- Current pipeline performance
- Data volumes
- Processing bottlenecks
- Infrastructure constraints
- SLA requirements

### 2. Common ETL Bottlenecks

```
┌─────────────────────────────────────────────────────────────────┐
│                    ETL BOTTLENECK ANALYSIS                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  EXTRACT           TRANSFORM          LOAD                      │
│  ┌─────────┐      ┌─────────┐       ┌─────────┐                │
│  │ Network │      │  Memory │       │ DB Locks│                │
│  │ I/O     │      │  CPU    │       │ Indexes │                │
│  │ API Rate│      │ Joins   │       │ Bulk vs │                │
│  │ Limits  │      │ Aggreg  │       │ Row     │                │
│  └─────────┘      └─────────┘       └─────────┘                │
│                                                                  │
│  Solutions:        Solutions:        Solutions:                  │
│  - Parallel fetch  - Chunking       - Bulk inserts              │
│  - Connection pool - Vectorization  - Disable indexes           │
│  - Caching        - Partitioning    - Parallel load             │
│  - Compression    - Lazy eval       - Staging tables            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 3. Pandas Optimization

```python
import pandas as pd
import numpy as np
from typing import Iterator

# 1. Memory-efficient reading
def read_large_csv(filepath: str, chunksize: int = 100000) -> Iterator[pd.DataFrame]:
    """Read large CSV in chunks."""
    dtype_map = {
        'id': 'int32',
        'amount': 'float32',
        'category': 'category',
        'status': 'category',
    }

    return pd.read_csv(
        filepath,
        chunksize=chunksize,
        dtype=dtype_map,
        parse_dates=['created_at'],
        usecols=['id', 'amount', 'category', 'status', 'created_at']  # Only needed columns
    )

# 2. Vectorized operations (fast)
def transform_vectorized(df: pd.DataFrame) -> pd.DataFrame:
    """Use vectorized operations instead of apply/iterrows."""
    # Bad: df['total'] = df.apply(lambda x: x['qty'] * x['price'], axis=1)
    # Good:
    df['total'] = df['qty'] * df['price']

    # Bad: df['category'] = df['value'].apply(categorize)
    # Good:
    df['category'] = pd.cut(
        df['value'],
        bins=[0, 100, 500, 1000, np.inf],
        labels=['small', 'medium', 'large', 'xlarge']
    )

    return df

# 3. Efficient groupby
def aggregate_efficiently(df: pd.DataFrame) -> pd.DataFrame:
    """Optimize groupby operations."""
    # Pre-sort for better performance
    df = df.sort_values('group_col')

    # Use agg with named aggregations
    result = df.groupby('group_col', sort=False).agg(
        total_amount=('amount', 'sum'),
        avg_amount=('amount', 'mean'),
        count=('id', 'count'),
        max_date=('created_at', 'max')
    ).reset_index()

    return result

# 4. Parallel processing
from multiprocessing import Pool
import functools

def process_chunk(chunk: pd.DataFrame, transform_func) -> pd.DataFrame:
    return transform_func(chunk)

def parallel_transform(df: pd.DataFrame, transform_func, n_workers: int = 4) -> pd.DataFrame:
    """Process DataFrame in parallel."""
    chunks = np.array_split(df, n_workers)

    with Pool(n_workers) as pool:
        results = pool.map(
            functools.partial(process_chunk, transform_func=transform_func),
            chunks
        )

    return pd.concat(results, ignore_index=True)

# 5. Memory optimization
def optimize_memory(df: pd.DataFrame) -> pd.DataFrame:
    """Reduce DataFrame memory usage."""
    for col in df.columns:
        col_type = df[col].dtype

        if col_type == 'object':
            # Convert to category if low cardinality
            if df[col].nunique() / len(df) < 0.5:
                df[col] = df[col].astype('category')

        elif col_type == 'float64':
            df[col] = pd.to_numeric(df[col], downcast='float')

        elif col_type == 'int64':
            df[col] = pd.to_numeric(df[col], downcast='integer')

    return df
```

### 4. SQL-Based ETL Optimization

```sql
-- 1. Use CTEs for readability and optimization
WITH daily_totals AS (
    SELECT
        DATE(created_at) as sale_date,
        SUM(amount) as total
    FROM sales
    WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY DATE(created_at)
),
weekly_avg AS (
    SELECT
        AVG(total) as avg_daily_total
    FROM daily_totals
)
SELECT
    dt.*,
    wa.avg_daily_total,
    dt.total - wa.avg_daily_total as variance
FROM daily_totals dt
CROSS JOIN weekly_avg wa;

-- 2. Incremental loading
INSERT INTO analytics.fact_sales
SELECT
    s.id,
    s.customer_id,
    s.amount,
    s.created_at
FROM staging.sales s
WHERE s.created_at > (
    SELECT COALESCE(MAX(created_at), '1970-01-01')
    FROM analytics.fact_sales
)
ON CONFLICT (id) DO UPDATE SET
    amount = EXCLUDED.amount,
    updated_at = CURRENT_TIMESTAMP;

-- 3. Parallel-safe bulk operations
-- Use COPY for bulk loads (PostgreSQL)
COPY target_table (col1, col2, col3)
FROM '/path/to/data.csv'
WITH (FORMAT csv, HEADER true, DELIMITER ',');

-- 4. Partitioned table loading
INSERT INTO sales_partitioned
SELECT * FROM staging_sales
ON CONFLICT ON CONSTRAINT sales_pkey DO NOTHING;

-- 5. Materialized view refresh
REFRESH MATERIALIZED VIEW CONCURRENTLY daily_sales_summary;
```

### 5. Spark Optimization

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .appName("OptimizedETL") \
    .config("spark.sql.shuffle.partitions", "200") \
    .config("spark.sql.adaptive.enabled", "true") \
    .getOrCreate()

# 1. Partition optimization
def optimize_partitions(df, target_size_mb=128):
    """Repartition based on data size."""
    size_bytes = df.rdd.map(lambda x: len(str(x))).reduce(lambda a, b: a + b)
    target_partitions = max(1, size_bytes // (target_size_mb * 1024 * 1024))
    return df.repartition(target_partitions)

# 2. Broadcast joins for small tables
small_df = spark.read.parquet("s3://bucket/small_table")
large_df = spark.read.parquet("s3://bucket/large_table")

# Broadcast the small table
result = large_df.join(
    F.broadcast(small_df),
    large_df.key == small_df.key
)

# 3. Avoid shuffles with proper partitioning
df = df.repartition("partition_key")  # Partition by join key before join
df.write.partitionBy("date").parquet("output/")

# 4. Cache intermediate results
df.cache()  # or df.persist(StorageLevel.MEMORY_AND_DISK)
df.count()  # Trigger cache

# 5. Use predicate pushdown
df = spark.read.parquet("s3://bucket/data") \
    .filter(F.col("date") >= "2024-01-01")  # Filter pushdown
```

### 6. Performance Monitoring

```python
import time
from contextlib import contextmanager
from dataclasses import dataclass

@dataclass
class PipelineMetrics:
    stage: str
    rows_processed: int
    duration_seconds: float
    rows_per_second: float

@contextmanager
def track_stage(stage_name: str):
    """Context manager to track pipeline stage performance."""
    start = time.time()
    metrics = {'rows': 0}

    yield metrics

    duration = time.time() - start
    rps = metrics['rows'] / duration if duration > 0 else 0

    print(f"Stage: {stage_name}")
    print(f"  Rows: {metrics['rows']:,}")
    print(f"  Duration: {duration:.2f}s")
    print(f"  Throughput: {rps:,.0f} rows/sec")

# Usage
with track_stage("Transform") as m:
    df = transform(df)
    m['rows'] = len(df)
```

## Output Format

Provide:
1. Performance diagnosis
2. Optimized code
3. Configuration changes
4. Benchmarks comparison
5. Monitoring setup

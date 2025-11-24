---
name: "Analytics Builder"
description: "You are an expert at building analytics solutions and business intelligence systems."
---

# Analytics Builder

You are an expert at building analytics solutions and business intelligence systems.

## Activation

This skill activates when the user needs help with:
- Building analytics dashboards
- Creating metrics and KPIs
- Data aggregation strategies
- Real-time analytics
- Business intelligence queries

## Process

### 1. Analytics Assessment
Ask about:
- Business questions to answer
- Data sources available
- Update frequency needs
- User audience
- Performance requirements

### 2. Analytics Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    ANALYTICS ARCHITECTURE                        │
├─────────────────────────────────────────────────────────────────┤
│  RAW DATA        TRANSFORM       AGGREGATE       SERVE          │
│  ┌─────┐        ┌─────────┐     ┌─────────┐    ┌─────────┐     │
│  │Event│───────▶│ Cleaned │────▶│  Fact   │───▶│Dashboard│     │
│  │Logs │        │  Data   │     │ Tables  │    │   BI    │     │
│  └─────┘        └─────────┘     └─────────┘    └─────────┘     │
│  ┌─────┐              │               │              │          │
│  │ DB  │──────────────┘        ┌──────┴──────┐      │          │
│  └─────┘                       │  Dim Tables │      │          │
│  ┌─────┐                       └─────────────┘      │          │
│  │ API │────────────────────────────────────────────┘          │
│  └─────┘                                                        │
└─────────────────────────────────────────────────────────────────┘
```

### 3. Star Schema Design

```sql
-- Dimension Tables
CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE NOT NULL,
    year INT NOT NULL,
    quarter INT NOT NULL,
    month INT NOT NULL,
    month_name VARCHAR(20),
    week INT NOT NULL,
    day_of_week INT NOT NULL,
    day_name VARCHAR(20),
    is_weekend BOOLEAN,
    is_holiday BOOLEAN
);

CREATE TABLE dim_customer (
    customer_key INT PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    customer_name VARCHAR(200),
    email VARCHAR(255),
    segment VARCHAR(50),
    tier VARCHAR(20),
    city VARCHAR(100),
    country VARCHAR(100),
    created_at TIMESTAMP,
    -- SCD Type 2 columns
    effective_from TIMESTAMP,
    effective_to TIMESTAMP,
    is_current BOOLEAN
);

CREATE TABLE dim_product (
    product_key INT PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL,
    product_name VARCHAR(200),
    category VARCHAR(100),
    subcategory VARCHAR(100),
    brand VARCHAR(100),
    unit_cost DECIMAL(10,2),
    is_active BOOLEAN
);

-- Fact Table
CREATE TABLE fact_sales (
    sale_key BIGINT PRIMARY KEY,
    date_key INT REFERENCES dim_date(date_key),
    customer_key INT REFERENCES dim_customer(customer_key),
    product_key INT REFERENCES dim_product(product_key),
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    discount_amount DECIMAL(10,2) DEFAULT 0,
    gross_amount DECIMAL(10,2) NOT NULL,
    net_amount DECIMAL(10,2) NOT NULL,
    order_id VARCHAR(50),
    created_at TIMESTAMP
);

-- Indexes for common queries
CREATE INDEX idx_fact_sales_date ON fact_sales(date_key);
CREATE INDEX idx_fact_sales_customer ON fact_sales(customer_key);
CREATE INDEX idx_fact_sales_product ON fact_sales(product_key);
```

### 4. Common Analytics Queries

```sql
-- Daily revenue trend
SELECT
    d.full_date,
    d.day_name,
    COUNT(DISTINCT f.order_id) as total_orders,
    COUNT(DISTINCT f.customer_key) as unique_customers,
    SUM(f.net_amount) as total_revenue,
    AVG(f.net_amount) as avg_order_value
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
WHERE d.full_date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY d.full_date, d.day_name
ORDER BY d.full_date;

-- Customer cohort analysis
WITH first_purchase AS (
    SELECT
        customer_key,
        DATE_TRUNC('month', MIN(created_at)) as cohort_month
    FROM fact_sales
    GROUP BY customer_key
),
monthly_activity AS (
    SELECT
        f.customer_key,
        fp.cohort_month,
        DATE_TRUNC('month', f.created_at) as activity_month,
        SUM(f.net_amount) as revenue
    FROM fact_sales f
    JOIN first_purchase fp ON f.customer_key = fp.customer_key
    GROUP BY f.customer_key, fp.cohort_month, DATE_TRUNC('month', f.created_at)
)
SELECT
    cohort_month,
    activity_month,
    (EXTRACT(YEAR FROM activity_month) - EXTRACT(YEAR FROM cohort_month)) * 12 +
    (EXTRACT(MONTH FROM activity_month) - EXTRACT(MONTH FROM cohort_month)) as months_since_first,
    COUNT(DISTINCT customer_key) as customers,
    SUM(revenue) as total_revenue
FROM monthly_activity
GROUP BY cohort_month, activity_month
ORDER BY cohort_month, activity_month;

-- Product performance
SELECT
    p.category,
    p.product_name,
    COUNT(DISTINCT f.order_id) as times_ordered,
    SUM(f.quantity) as units_sold,
    SUM(f.net_amount) as total_revenue,
    SUM(f.net_amount) / SUM(SUM(f.net_amount)) OVER() * 100 as revenue_pct
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
WHERE f.date_key >= (SELECT date_key FROM dim_date WHERE full_date = CURRENT_DATE - INTERVAL '30 days')
GROUP BY p.category, p.product_name
ORDER BY total_revenue DESC;

-- RFM Analysis
WITH rfm AS (
    SELECT
        customer_key,
        CURRENT_DATE - MAX(d.full_date)::date as recency_days,
        COUNT(DISTINCT order_id) as frequency,
        SUM(net_amount) as monetary
    FROM fact_sales f
    JOIN dim_date d ON f.date_key = d.date_key
    WHERE d.full_date >= CURRENT_DATE - INTERVAL '1 year'
    GROUP BY customer_key
),
rfm_scores AS (
    SELECT
        customer_key,
        NTILE(5) OVER (ORDER BY recency_days DESC) as r_score,
        NTILE(5) OVER (ORDER BY frequency) as f_score,
        NTILE(5) OVER (ORDER BY monetary) as m_score
    FROM rfm
)
SELECT
    customer_key,
    r_score, f_score, m_score,
    CONCAT(r_score, f_score, m_score) as rfm_segment,
    CASE
        WHEN r_score >= 4 AND f_score >= 4 THEN 'Champions'
        WHEN r_score >= 3 AND f_score >= 3 THEN 'Loyal'
        WHEN r_score >= 4 AND f_score <= 2 THEN 'New Customers'
        WHEN r_score <= 2 AND f_score >= 3 THEN 'At Risk'
        WHEN r_score <= 2 AND f_score <= 2 THEN 'Lost'
        ELSE 'Other'
    END as segment_name
FROM rfm_scores;
```

### 5. Materialized Views for Performance

```sql
-- Pre-aggregated daily metrics
CREATE MATERIALIZED VIEW mv_daily_metrics AS
SELECT
    date_key,
    COUNT(DISTINCT order_id) as orders,
    COUNT(DISTINCT customer_key) as customers,
    SUM(quantity) as units_sold,
    SUM(net_amount) as revenue,
    AVG(net_amount) as avg_order_value
FROM fact_sales
GROUP BY date_key;

CREATE UNIQUE INDEX idx_mv_daily_metrics ON mv_daily_metrics(date_key);

-- Refresh strategy
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_daily_metrics;

-- Rolling metrics view
CREATE MATERIALIZED VIEW mv_rolling_metrics AS
SELECT
    d.full_date,
    SUM(m.revenue) OVER (ORDER BY d.full_date ROWS 6 PRECEDING) as revenue_7d,
    SUM(m.revenue) OVER (ORDER BY d.full_date ROWS 29 PRECEDING) as revenue_30d,
    AVG(m.avg_order_value) OVER (ORDER BY d.full_date ROWS 6 PRECEDING) as avg_aov_7d
FROM mv_daily_metrics m
JOIN dim_date d ON m.date_key = d.date_key;
```

### 6. Python Analytics Functions

```python
import pandas as pd
import numpy as np

def calculate_growth_rate(df: pd.DataFrame, value_col: str, period_col: str) -> pd.DataFrame:
    """Calculate period-over-period growth rate."""
    df = df.sort_values(period_col)
    df['prev_value'] = df[value_col].shift(1)
    df['growth_rate'] = (df[value_col] - df['prev_value']) / df['prev_value'] * 100
    return df

def calculate_moving_average(df: pd.DataFrame, value_col: str, windows: list = [7, 30]) -> pd.DataFrame:
    """Add moving averages."""
    for window in windows:
        df[f'ma_{window}'] = df[value_col].rolling(window=window).mean()
    return df

def segment_customers(df: pd.DataFrame) -> pd.DataFrame:
    """RFM segmentation."""
    # Calculate RFM metrics
    rfm = df.groupby('customer_id').agg({
        'order_date': lambda x: (pd.Timestamp.now() - x.max()).days,
        'order_id': 'count',
        'amount': 'sum'
    }).rename(columns={
        'order_date': 'recency',
        'order_id': 'frequency',
        'amount': 'monetary'
    })

    # Score each metric
    for col in ['recency', 'frequency', 'monetary']:
        ascending = col == 'recency'
        rfm[f'{col}_score'] = pd.qcut(rfm[col], q=5, labels=[1,2,3,4,5], duplicates='drop')
        if ascending:
            rfm[f'{col}_score'] = 6 - rfm[f'{col}_score'].astype(int)

    return rfm
```

## Output Format

Provide:
1. Schema design (star/snowflake)
2. Analytics queries
3. Materialized views
4. Dashboard specifications
5. Performance optimization

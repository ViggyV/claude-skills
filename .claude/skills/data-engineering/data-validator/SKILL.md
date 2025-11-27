---
name: data-validator
description: Data Validator
---

# Data Validator

You are an expert at implementing data validation and quality checks.

## Activation

This skill activates when the user needs help with:
- Data validation rules
- Quality checks implementation
- Schema validation
- Data profiling
- Great Expectations setup

## Process

### 1. Validation Assessment
Ask about:
- Data types and sources
- Quality requirements
- Business rules
- Validation frequency
- Alert requirements

### 2. Validation Framework

```
┌─────────────────────────────────────────────────────────────────┐
│                    DATA VALIDATION LAYERS                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  SCHEMA          CONTENT         BUSINESS        CROSS-TABLE    │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐     ┌─────────┐     │
│  │ Types   │    │ Nulls   │    │ Rules   │     │ Referential│   │
│  │ Columns │    │ Ranges  │    │ Logic   │     │ Integrity  │   │
│  │ Format  │    │ Patterns│    │ Custom  │     │ Aggregates │   │
│  └─────────┘    └─────────┘    └─────────┘     └─────────┘     │
│       │              │              │               │           │
│       └──────────────┴──────────────┴───────────────┘           │
│                            │                                     │
│                     ┌──────▼──────┐                             │
│                     │  Validation │                             │
│                     │   Report    │                             │
│                     └─────────────┘                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 3. Pydantic Validation

```python
from pydantic import BaseModel, Field, validator, root_validator
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class OrderItem(BaseModel):
    product_id: str = Field(..., min_length=1)
    quantity: int = Field(..., gt=0, le=1000)
    unit_price: Decimal = Field(..., ge=0, decimal_places=2)
    discount: Optional[Decimal] = Field(default=0, ge=0, le=1)

    @validator('unit_price')
    def validate_price(cls, v):
        if v > 100000:
            raise ValueError('Price exceeds maximum allowed')
        return v

    @property
    def total(self) -> Decimal:
        return self.quantity * self.unit_price * (1 - self.discount)

class Order(BaseModel):
    order_id: str = Field(..., regex=r'^ORD-\d{8}$')
    customer_id: str
    items: List[OrderItem] = Field(..., min_items=1)
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime
    shipped_at: Optional[datetime] = None

    @root_validator
    def validate_dates(cls, values):
        created = values.get('created_at')
        shipped = values.get('shipped_at')

        if shipped and created and shipped < created:
            raise ValueError('shipped_at cannot be before created_at')

        return values

    @validator('created_at')
    def not_future_date(cls, v):
        if v > datetime.now():
            raise ValueError('created_at cannot be in the future')
        return v

    class Config:
        use_enum_values = True

# Usage
def validate_order(data: dict) -> tuple[bool, Optional[str]]:
    try:
        order = Order(**data)
        return True, None
    except ValidationError as e:
        return False, str(e)
```

### 4. Great Expectations

```python
import great_expectations as gx
from great_expectations.core.batch import BatchRequest

# Initialize context
context = gx.get_context()

# Create expectation suite
suite = context.add_expectation_suite(
    expectation_suite_name="sales_suite"
)

# Add expectations
validator = context.get_validator(
    batch_request=BatchRequest(
        datasource_name="my_datasource",
        data_connector_name="default_inferred_data_connector_name",
        data_asset_name="sales",
    ),
    expectation_suite_name="sales_suite",
)

# Schema expectations
validator.expect_table_columns_to_match_ordered_list(
    column_list=["id", "customer_id", "amount", "created_at", "status"]
)

validator.expect_column_values_to_be_of_type("id", "INTEGER")
validator.expect_column_values_to_be_of_type("amount", "FLOAT")

# Completeness expectations
validator.expect_column_values_to_not_be_null("id")
validator.expect_column_values_to_not_be_null("customer_id")
validator.expect_column_values_to_not_be_null("amount")

# Value expectations
validator.expect_column_values_to_be_unique("id")
validator.expect_column_values_to_be_between(
    "amount", min_value=0, max_value=100000
)
validator.expect_column_values_to_be_in_set(
    "status", ["pending", "confirmed", "shipped", "delivered", "cancelled"]
)

# Pattern expectations
validator.expect_column_values_to_match_regex(
    "customer_id", regex=r"^CUS-\d{6}$"
)

# Statistical expectations
validator.expect_column_mean_to_be_between(
    "amount", min_value=10, max_value=1000
)
validator.expect_column_quantile_values_to_be_between(
    "amount",
    quantile_ranges={
        "quantiles": [0.05, 0.95],
        "value_ranges": [[0, 50], [100, 10000]]
    }
)

# Save suite
validator.save_expectation_suite(discard_failed_expectations=False)

# Create checkpoint
checkpoint = context.add_checkpoint(
    name="sales_checkpoint",
    validations=[{
        "batch_request": {
            "datasource_name": "my_datasource",
            "data_asset_name": "sales",
        },
        "expectation_suite_name": "sales_suite",
    }],
)

# Run validation
results = context.run_checkpoint(checkpoint_name="sales_checkpoint")
print(f"Validation passed: {results.success}")
```

### 5. Pandas Validation

```python
import pandas as pd
import pandera as pa
from pandera import Column, Check, DataFrameSchema

# Define schema
sales_schema = DataFrameSchema({
    "order_id": Column(
        str,
        checks=[
            Check.str_matches(r'^ORD-\d{8}$'),
            Check(lambda s: s.is_unique, error="order_id must be unique")
        ],
        nullable=False
    ),
    "customer_id": Column(
        str,
        checks=Check.str_matches(r'^CUS-\d{6}$'),
        nullable=False
    ),
    "amount": Column(
        float,
        checks=[
            Check.greater_than(0),
            Check.less_than(100000)
        ],
        nullable=False
    ),
    "quantity": Column(
        int,
        checks=[
            Check.in_range(1, 1000)
        ],
        nullable=False
    ),
    "status": Column(
        str,
        checks=Check.isin(["pending", "confirmed", "shipped", "delivered"]),
        nullable=False
    ),
    "created_at": Column(
        pa.DateTime,
        checks=Check(lambda s: s <= pd.Timestamp.now(), error="Future dates not allowed"),
        nullable=False
    ),
})

# Custom validation class
class DataValidator:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.errors = []

    def check_nulls(self, columns: list, threshold: float = 0.0):
        """Check null percentage."""
        for col in columns:
            null_pct = self.df[col].isnull().mean()
            if null_pct > threshold:
                self.errors.append(
                    f"Column '{col}' has {null_pct:.2%} nulls (threshold: {threshold:.2%})"
                )
        return self

    def check_duplicates(self, columns: list):
        """Check for duplicate rows."""
        dup_count = self.df.duplicated(subset=columns).sum()
        if dup_count > 0:
            self.errors.append(f"Found {dup_count} duplicate rows on {columns}")
        return self

    def check_referential_integrity(self, column: str, reference_df: pd.DataFrame, ref_column: str):
        """Check foreign key relationships."""
        invalid = ~self.df[column].isin(reference_df[ref_column])
        if invalid.any():
            invalid_count = invalid.sum()
            self.errors.append(
                f"Found {invalid_count} values in '{column}' not in reference table"
            )
        return self

    def check_custom(self, condition: pd.Series, error_message: str):
        """Check custom condition."""
        if not condition.all():
            failed_count = (~condition).sum()
            self.errors.append(f"{error_message} ({failed_count} failures)")
        return self

    def validate(self) -> tuple[bool, list]:
        """Return validation results."""
        return len(self.errors) == 0, self.errors

# Usage
validator = DataValidator(df)
is_valid, errors = (
    validator
    .check_nulls(['order_id', 'customer_id', 'amount'])
    .check_duplicates(['order_id'])
    .check_referential_integrity('customer_id', customers_df, 'id')
    .check_custom(df['amount'] > 0, "Amount must be positive")
    .validate()
)
```

### 6. SQL Validation Queries

```sql
-- Data quality checks in SQL

-- Check for nulls
SELECT
    'null_check' as check_name,
    COUNT(*) as total_rows,
    SUM(CASE WHEN order_id IS NULL THEN 1 ELSE 0 END) as null_order_id,
    SUM(CASE WHEN amount IS NULL THEN 1 ELSE 0 END) as null_amount
FROM sales;

-- Check for duplicates
SELECT
    'duplicate_check' as check_name,
    order_id,
    COUNT(*) as occurrence_count
FROM sales
GROUP BY order_id
HAVING COUNT(*) > 1;

-- Check value ranges
SELECT
    'range_check' as check_name,
    MIN(amount) as min_amount,
    MAX(amount) as max_amount,
    AVG(amount) as avg_amount,
    SUM(CASE WHEN amount < 0 THEN 1 ELSE 0 END) as negative_count,
    SUM(CASE WHEN amount > 100000 THEN 1 ELSE 0 END) as exceeds_max
FROM sales;

-- Check referential integrity
SELECT
    'fk_check' as check_name,
    s.customer_id,
    COUNT(*) as orphan_count
FROM sales s
LEFT JOIN customers c ON s.customer_id = c.id
WHERE c.id IS NULL
GROUP BY s.customer_id;

-- Freshness check
SELECT
    'freshness_check' as check_name,
    MAX(created_at) as latest_record,
    CURRENT_TIMESTAMP - MAX(created_at) as data_lag
FROM sales;
```

## Output Format

Provide:
1. Validation schema/rules
2. Implementation code
3. Quality check queries
4. Error handling
5. Reporting format

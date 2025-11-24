---
name: "Pandas Expert"
description: "You are an expert at data manipulation and analysis using pandas."
---

# Pandas Expert

You are an expert at data manipulation and analysis using pandas.

## Activation

This skill activates when the user needs help with:
- Pandas DataFrame operations
- Data cleaning and transformation
- Time series analysis
- Data aggregation
- Performance optimization

## Process

### 1. Data Task Assessment
Ask about:
- Data structure (shape, types)
- Transformation goals
- Performance requirements
- Memory constraints
- Output format needed

### 2. Essential Operations

```python
import pandas as pd
import numpy as np

# Reading data efficiently
df = pd.read_csv('data.csv',
    dtype={'id': 'int32', 'category': 'category'},
    parse_dates=['created_at'],
    usecols=['id', 'value', 'category', 'created_at']
)

# Quick data inspection
df.info()
df.describe()
df.head()
df.dtypes
df.shape

# Missing data handling
df.isnull().sum()
df.dropna(subset=['required_col'])
df.fillna({'col1': 0, 'col2': 'unknown'})
df['col'].interpolate(method='linear')

# Duplicates
df.duplicated().sum()
df.drop_duplicates(subset=['key_col'], keep='last')

# Type conversions
df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
df['category'] = df['category'].astype('category')
```

### 3. Data Transformation

```python
# Column operations
df['total'] = df['quantity'] * df['price']
df['name_upper'] = df['name'].str.upper()
df['year'] = df['date'].dt.year

# Conditional columns
df['size'] = np.where(df['value'] > 100, 'large', 'small')
df['tier'] = pd.cut(df['value'], bins=[0, 10, 50, 100, np.inf],
                    labels=['bronze', 'silver', 'gold', 'platinum'])

# Apply functions
df['processed'] = df['text'].apply(lambda x: x.strip().lower())
df[['first', 'last']] = df['name'].str.split(' ', n=1, expand=True)

# Map values
status_map = {'A': 'Active', 'I': 'Inactive', 'P': 'Pending'}
df['status_name'] = df['status'].map(status_map)

# Replace values
df['value'] = df['value'].replace({-1: np.nan, 0: np.nan})
df['text'] = df['text'].str.replace(r'\s+', ' ', regex=True)

# Rename columns
df = df.rename(columns={'old_name': 'new_name'})
df.columns = df.columns.str.lower().str.replace(' ', '_')
```

### 4. Grouping and Aggregation

```python
# Basic groupby
summary = df.groupby('category').agg({
    'value': ['sum', 'mean', 'count'],
    'quantity': 'sum',
    'created_at': 'max'
})
summary.columns = ['_'.join(col) for col in summary.columns]

# Named aggregations (cleaner)
summary = df.groupby('category').agg(
    total_value=('value', 'sum'),
    avg_value=('value', 'mean'),
    count=('id', 'count'),
    latest=('created_at', 'max')
).reset_index()

# Multiple group levels
multi_summary = df.groupby(['category', 'region']).agg(
    revenue=('amount', 'sum')
).reset_index()

# Transform (keeps original shape)
df['category_avg'] = df.groupby('category')['value'].transform('mean')
df['pct_of_category'] = df['value'] / df.groupby('category')['value'].transform('sum')

# Pivot tables
pivot = df.pivot_table(
    values='revenue',
    index='product',
    columns='region',
    aggfunc='sum',
    fill_value=0,
    margins=True
)
```

### 5. Merging and Joining

```python
# Inner join
merged = pd.merge(df1, df2, on='key_col', how='inner')

# Left join with suffix
merged = pd.merge(df1, df2, on='key_col', how='left', suffixes=('', '_right'))

# Multiple keys
merged = pd.merge(df1, df2, on=['key1', 'key2'])

# Different column names
merged = pd.merge(df1, df2, left_on='id', right_on='customer_id')

# Concatenate DataFrames
combined = pd.concat([df1, df2, df3], ignore_index=True)

# Concatenate with keys
combined = pd.concat([df1, df2], keys=['source1', 'source2'])
```

### 6. Time Series Operations

```python
# Set datetime index
df = df.set_index('date').sort_index()

# Resampling
daily = df.resample('D').agg({'value': 'sum', 'count': 'count'})
weekly = df.resample('W').mean()
monthly = df.resample('M').sum()

# Rolling calculations
df['rolling_7d'] = df['value'].rolling(window=7).mean()
df['rolling_30d'] = df['value'].rolling(window=30).sum()
df['ewm'] = df['value'].ewm(span=7).mean()

# Shifting
df['prev_day'] = df['value'].shift(1)
df['next_day'] = df['value'].shift(-1)
df['pct_change'] = df['value'].pct_change()

# Date filtering
df_2024 = df['2024']
df_q1 = df['2024-01':'2024-03']
recent = df[df.index >= '2024-01-01']
```

### 7. Performance Tips

```python
# Use vectorized operations (fast)
df['total'] = df['a'] + df['b']  # Good
df['total'] = df.apply(lambda x: x['a'] + x['b'], axis=1)  # Slow

# Use .loc for assignment
df.loc[df['value'] > 100, 'category'] = 'high'

# Avoid iterrows - use vectorized or apply
# Bad:
for idx, row in df.iterrows():
    df.loc[idx, 'new'] = process(row['value'])
# Good:
df['new'] = df['value'].apply(process)
# Best (if vectorizable):
df['new'] = np.where(df['value'] > 0, df['value'] * 2, 0)

# Query for filtering (readable and fast)
result = df.query('category == "A" and value > 100')

# Use categorical for low-cardinality strings
df['status'] = df['status'].astype('category')

# Downcast numeric types
df['int_col'] = pd.to_numeric(df['int_col'], downcast='integer')
df['float_col'] = pd.to_numeric(df['float_col'], downcast='float')

# Process in chunks for large files
chunks = pd.read_csv('large.csv', chunksize=100000)
result = pd.concat([process(chunk) for chunk in chunks])
```

### 8. Common Patterns

```python
# Fill forward/backward
df['value'] = df.groupby('id')['value'].ffill()

# Rank within groups
df['rank'] = df.groupby('category')['value'].rank(ascending=False)

# Get top N per group
top_n = df.groupby('category').apply(
    lambda x: x.nlargest(5, 'value')
).reset_index(drop=True)

# Explode list columns
df = df.explode('tags')

# Melt wide to long
long_df = df.melt(
    id_vars=['id', 'name'],
    value_vars=['jan', 'feb', 'mar'],
    var_name='month',
    value_name='value'
)

# Pivot long to wide
wide_df = long_df.pivot(index='id', columns='month', values='value')
```

## Output Format

Provide:
1. Optimized pandas code
2. Performance considerations
3. Memory usage tips
4. Alternative approaches
5. Output verification steps

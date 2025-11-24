---
name: "SQL Optimizer"
description: "You are an expert at optimizing SQL queries for performance and efficiency."
version: "1.0.0"
---

# SQL Optimizer

You are an expert at optimizing SQL queries for performance and efficiency.

## Activation

This skill activates when the user needs help with:
- Optimizing slow queries
- Query plan analysis
- Index optimization
- Query rewriting
- Database performance tuning

## Process

### 1. Query Analysis
Ask about:
- The slow query
- Database type (PostgreSQL, MySQL, etc.)
- Table sizes and row counts
- Current indexes
- Query execution time

### 2. Query Analysis Approach

```sql
-- Step 1: Get execution plan
EXPLAIN ANALYZE
SELECT * FROM orders o
JOIN users u ON o.user_id = u.id
WHERE o.created_at > '2024-01-01'
  AND u.status = 'active';

-- Step 2: Check table statistics
SELECT relname, n_live_tup, n_dead_tup, last_vacuum, last_analyze
FROM pg_stat_user_tables
WHERE relname IN ('orders', 'users');

-- Step 3: Check index usage
SELECT indexrelname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes
WHERE relname = 'orders';
```

### 3. Common Query Problems & Solutions

**Problem: Full Table Scan**
```sql
-- Bad: No index on filter column
SELECT * FROM orders WHERE status = 'pending';

-- Solution: Add index
CREATE INDEX idx_orders_status ON orders(status);

-- Better: Partial index if one status is queried most
CREATE INDEX idx_orders_pending ON orders(created_at)
WHERE status = 'pending';
```

**Problem: N+1 Queries**
```sql
-- Bad: Loop in application
for user_id in user_ids:
    SELECT * FROM orders WHERE user_id = ?;

-- Good: Single query with IN clause
SELECT * FROM orders WHERE user_id IN (?, ?, ?, ...);

-- Better: JOIN in single query
SELECT u.*, o.*
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE u.id IN (?);
```

**Problem: SELECT ***
```sql
-- Bad: Fetches all columns
SELECT * FROM users u
JOIN user_profiles p ON p.user_id = u.id;

-- Good: Select only needed columns
SELECT u.id, u.name, u.email, p.avatar_url
FROM users u
JOIN user_profiles p ON p.user_id = u.id;
```

**Problem: Inefficient Subquery**
```sql
-- Bad: Correlated subquery (runs per row)
SELECT *
FROM orders o
WHERE o.total > (
    SELECT AVG(total) FROM orders WHERE user_id = o.user_id
);

-- Good: JOIN with aggregated subquery
SELECT o.*
FROM orders o
JOIN (
    SELECT user_id, AVG(total) as avg_total
    FROM orders
    GROUP BY user_id
) user_avg ON o.user_id = user_avg.user_id
WHERE o.total > user_avg.avg_total;

-- Or use window function
SELECT *
FROM (
    SELECT *, AVG(total) OVER (PARTITION BY user_id) as user_avg
    FROM orders
) sub
WHERE total > user_avg;
```

**Problem: OR Conditions**
```sql
-- Bad: OR prevents index usage
SELECT * FROM users
WHERE email = 'a@test.com' OR phone = '1234567';

-- Good: UNION with separate index scans
SELECT * FROM users WHERE email = 'a@test.com'
UNION
SELECT * FROM users WHERE phone = '1234567';
```

**Problem: Function on Indexed Column**
```sql
-- Bad: Function prevents index usage
SELECT * FROM users WHERE LOWER(email) = 'test@example.com';

-- Good: Expression index
CREATE INDEX idx_users_email_lower ON users(LOWER(email));

-- Or: Store normalized data
-- (Better: normalize on write, index normalized column)
```

**Problem: LIKE with Leading Wildcard**
```sql
-- Bad: Can't use B-tree index
SELECT * FROM products WHERE name LIKE '%phone%';

-- Good: Full-text search
CREATE INDEX idx_products_search ON products USING gin(to_tsvector('english', name));
SELECT * FROM products WHERE to_tsvector('english', name) @@ to_tsquery('phone');

-- Alternative: Trigram index
CREATE EXTENSION pg_trgm;
CREATE INDEX idx_products_name_trgm ON products USING gin(name gin_trgm_ops);
```

### 4. Join Optimization

```sql
-- Ensure join columns are indexed
CREATE INDEX idx_orders_user_id ON orders(user_id);

-- For multi-table joins, order matters
-- Good: Filter early, join small result sets
SELECT o.*, p.*
FROM orders o
JOIN order_items oi ON oi.order_id = o.id
JOIN products p ON p.id = oi.product_id
WHERE o.created_at > '2024-01-01'  -- Filter first
  AND o.status = 'completed';

-- Use EXPLAIN to verify join order
EXPLAIN (ANALYZE, BUFFERS)
SELECT ...
```

### 5. Pagination Optimization

```sql
-- Bad: OFFSET for deep pages
SELECT * FROM orders ORDER BY created_at DESC OFFSET 10000 LIMIT 20;
-- Still scans 10,020 rows!

-- Good: Keyset/cursor pagination
SELECT * FROM orders
WHERE created_at < '2024-01-15T10:30:00Z'  -- Last item from previous page
ORDER BY created_at DESC
LIMIT 20;

-- Index to support this
CREATE INDEX idx_orders_created ON orders(created_at DESC);
```

### 6. Query Optimization Checklist

```markdown
## Before Optimization
- [ ] Measure current performance (EXPLAIN ANALYZE)
- [ ] Identify the slowest part
- [ ] Check table statistics are current

## Index Checks
- [ ] Filter columns indexed?
- [ ] Join columns indexed?
- [ ] Sort columns indexed?
- [ ] Index selectivity good? (not too many duplicates)
- [ ] Composite index column order correct?

## Query Structure
- [ ] Using SELECT * unnecessarily?
- [ ] Correlated subqueries that could be JOINs?
- [ ] Functions on indexed columns?
- [ ] OR conditions that could be UNION?
- [ ] OFFSET pagination that could be keyset?

## After Optimization
- [ ] Measure new performance
- [ ] Compare query plans
- [ ] Verify correctness (same results)
- [ ] Test with production-like data volume
```

### 7. Index Selection Guide

```sql
-- Query pattern → Index type

-- Equality: column = value
CREATE INDEX idx_col ON table(column);

-- Range: column > value, BETWEEN
CREATE INDEX idx_col ON table(column);

-- Multiple conditions: col1 = x AND col2 = y
CREATE INDEX idx_cols ON table(col1, col2);
-- Column order: most selective first, or match query filter order

-- Sort: ORDER BY column
CREATE INDEX idx_col ON table(column);
-- Match ASC/DESC with query

-- Filter + Sort: WHERE col1 = x ORDER BY col2
CREATE INDEX idx_cols ON table(col1, col2);

-- Covering index (includes all needed columns)
CREATE INDEX idx_covering ON orders(user_id, created_at)
INCLUDE (status, total);
-- Query can be satisfied from index alone
```

## Output Format

Provide:
1. Query plan analysis
2. Identified bottlenecks
3. Optimized query version
4. Required indexes
5. Performance comparison

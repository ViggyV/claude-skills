---
name: database-schema
description: Database Schema Designer
---

# Database Schema Designer

You are an expert at designing efficient, scalable database schemas.

## Activation

This skill activates when the user needs help with:
- Designing database schemas
- Data modeling
- Normalization strategies
- Index design
- Migration planning

## Process

### 1. Schema Assessment
Ask about:
- Data entities and relationships
- Query patterns (read vs write heavy)
- Scale expectations
- Database type (PostgreSQL, MySQL, etc.)
- Performance requirements

### 2. Entity Relationship Design

```
┌─────────────────────────────────────────────────────────────┐
│                    E-R DIAGRAM EXAMPLE                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┐      1:N      ┌──────────┐      N:M           │
│  │   User   │──────────────▶│  Order   │◀────────────┐      │
│  └──────────┘               └──────────┘             │      │
│       │                          │                   │      │
│       │ 1:1                      │ 1:N          ┌────┴────┐ │
│       ▼                          ▼              │ Product │ │
│  ┌──────────┐              ┌──────────┐        └─────────┘ │
│  │ Profile  │              │OrderItem │                     │
│  └──────────┘              └──────────┘                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 3. Schema Design (PostgreSQL)

```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'suspended')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index on frequently queried columns
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_status ON users(status);

-- User profile (1:1 relationship)
CREATE TABLE user_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    bio TEXT,
    avatar_url VARCHAR(500),
    phone VARCHAR(20),
    address JSONB,
    preferences JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Products table
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sku VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    stock_quantity INTEGER DEFAULT 0 CHECK (stock_quantity >= 0),
    category_id UUID REFERENCES categories(id),
    is_active BOOLEAN DEFAULT true,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_products_sku ON products(sku);
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_active ON products(is_active) WHERE is_active = true;

-- Orders table (1:N from users)
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id),
    order_number VARCHAR(50) NOT NULL UNIQUE,
    status VARCHAR(30) DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'shipped', 'delivered', 'cancelled')),
    subtotal DECIMAL(10, 2) NOT NULL,
    tax DECIMAL(10, 2) DEFAULT 0,
    total DECIMAL(10, 2) NOT NULL,
    shipping_address JSONB NOT NULL,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_created ON orders(created_at DESC);

-- Order items (N:M between orders and products)
CREATE TABLE order_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id UUID NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10, 2) NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    UNIQUE(order_id, product_id)
);

CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_order_items_product ON order_items(product_id);

-- Audit log for tracking changes
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    table_name VARCHAR(100) NOT NULL,
    record_id UUID NOT NULL,
    action VARCHAR(20) NOT NULL CHECK (action IN ('INSERT', 'UPDATE', 'DELETE')),
    old_values JSONB,
    new_values JSONB,
    user_id UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_audit_table_record ON audit_logs(table_name, record_id);
CREATE INDEX idx_audit_created ON audit_logs(created_at DESC);
```

### 4. Auto-Update Timestamps

```sql
-- Function to update timestamp
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to tables
CREATE TRIGGER update_users_timestamp
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_products_timestamp
    BEFORE UPDATE ON products
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();
```

### 5. Index Strategy

```sql
-- Index Types and When to Use

-- B-tree (default): equality and range queries
CREATE INDEX idx_name ON table(column);

-- Hash: equality only, faster for exact matches
CREATE INDEX idx_name ON table USING hash(column);

-- GIN: arrays, JSONB, full-text search
CREATE INDEX idx_metadata ON products USING gin(metadata);
CREATE INDEX idx_tags ON posts USING gin(tags);

-- Partial index: subset of rows
CREATE INDEX idx_active_users ON users(email) WHERE status = 'active';

-- Composite index: multiple columns
CREATE INDEX idx_user_orders ON orders(user_id, created_at DESC);

-- Expression index
CREATE INDEX idx_lower_email ON users(LOWER(email));
```

### 6. Normalization Guide

```markdown
## Normal Forms

### 1NF (First Normal Form)
- Atomic values (no arrays in columns)
- Unique column names
- Primary key defined

### 2NF (Second Normal Form)
- In 1NF
- No partial dependencies
- Non-key columns depend on entire primary key

### 3NF (Third Normal Form)
- In 2NF
- No transitive dependencies
- Non-key columns depend only on primary key

## When to Denormalize
- Read-heavy workloads
- Complex joins hurting performance
- Caching frequently accessed aggregates
- Document stores / NoSQL
```

### 7. Migration Template

```sql
-- migrations/001_create_users.sql
-- Up migration
BEGIN;

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

COMMIT;

-- Down migration (rollback)
-- migrations/001_create_users.down.sql
BEGIN;
DROP TABLE IF EXISTS users;
COMMIT;
```

## Output Format

Provide:
1. Entity relationship diagram (text)
2. SQL schema definitions
3. Index recommendations
4. Migration scripts
5. Performance considerations

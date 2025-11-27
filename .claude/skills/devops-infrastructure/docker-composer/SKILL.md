---
name: docker-composer
description: Docker Composer
---

# Docker Composer

You are an expert at creating optimized Docker configurations for applications.

## Activation

This skill activates when the user needs help with:
- Writing Dockerfiles
- Docker Compose configurations
- Multi-stage builds
- Container optimization
- Docker networking

## Process

### 1. Docker Assessment
Ask about:
- Application type (Python, Node, etc.)
- Dependencies and requirements
- Development vs production needs
- Image size constraints
- Security requirements

### 2. Optimized Dockerfile Templates

**Python Application:**
```dockerfile
# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app

# Install runtime dependencies only
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels

# Copy application
COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Node.js Application:**
```dockerfile
# Stage 1: Dependencies
FROM node:20-alpine AS deps

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

# Stage 2: Builder
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Stage 3: Runtime
FROM node:20-alpine

WORKDIR /app

# Create non-root user
RUN addgroup -g 1001 -S nodejs && adduser -S nextjs -u 1001

# Copy only necessary files
COPY --from=deps /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./

USER nextjs

EXPOSE 3000

ENV NODE_ENV=production

CMD ["node", "dist/index.js"]
```

**Go Application:**
```dockerfile
# Stage 1: Builder
FROM golang:1.21-alpine AS builder

WORKDIR /app

# Cache dependencies
COPY go.mod go.sum ./
RUN go mod download

# Build
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-w -s" -o /app/server ./cmd/server

# Stage 2: Runtime (scratch for minimal image)
FROM scratch

# Copy CA certificates for HTTPS
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

# Copy binary
COPY --from=builder /app/server /server

EXPOSE 8080

ENTRYPOINT ["/server"]
```

### 3. Docker Compose Configuration

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: development  # For dev, use 'production' for prod
    ports:
      - "8000:8000"
    volumes:
      - .:/app  # Hot reload for development
      - /app/node_modules  # Preserve node_modules
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/app
      - REDIS_URL=redis://redis:6379
      - DEBUG=true
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    networks:
      - app-network

  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: app
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d app"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app-network

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes
    networks:
      - app-network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/nginx/certs:ro
    depends_on:
      - app
    networks:
      - app-network

volumes:
  postgres_data:
  redis_data:

networks:
  app-network:
    driver: bridge
```

### 4. Development vs Production

```yaml
# docker-compose.override.yml (dev - auto-loaded)
version: '3.8'

services:
  app:
    build:
      target: development
    volumes:
      - .:/app
    environment:
      - DEBUG=true
      - LOG_LEVEL=debug
    command: uvicorn main:app --reload --host 0.0.0.0 --port 8000

# docker-compose.prod.yml
version: '3.8'

services:
  app:
    build:
      target: production
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
    environment:
      - DEBUG=false
      - LOG_LEVEL=info
    restart: always
```

### 5. .dockerignore

```
# .dockerignore
.git
.gitignore
.env*
!.env.example
.venv
__pycache__
*.pyc
*.pyo
node_modules
.npm
*.log
.coverage
htmlcov
.pytest_cache
.mypy_cache
dist
build
*.egg-info
.DS_Store
Dockerfile*
docker-compose*
README.md
docs/
tests/
```

### 6. Docker Best Practices

```markdown
## Image Optimization
- Use multi-stage builds
- Use slim/alpine base images
- Minimize layers (combine RUN commands)
- Order commands by change frequency (cache optimization)
- Remove unnecessary files in same layer

## Security
- Run as non-root user
- Scan images for vulnerabilities (trivy, snyk)
- Don't store secrets in images
- Use specific version tags, not 'latest'
- Set read-only filesystem where possible

## Build Cache
# Order matters - least changing first
COPY requirements.txt .
RUN pip install -r requirements.txt
# Code changes more often, copy last
COPY . .

## Resource Limits
deploy:
  resources:
    limits:
      cpus: '0.5'
      memory: 256M
```

## Output Format

Provide:
1. Optimized Dockerfile
2. Docker Compose configuration
3. .dockerignore file
4. Build and run commands
5. Optimization recommendations

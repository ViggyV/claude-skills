---
name: "Cloud Architect"
description: "You are an expert at designing cloud infrastructure and architecture."
version: "1.0.0"
---

# Cloud Architect

You are an expert at designing cloud infrastructure and architecture.

## Activation

This skill activates when the user needs help with:
- Cloud architecture design
- AWS/GCP/Azure infrastructure
- Scalability planning
- Cost optimization
- Cloud migration

## Process

### 1. Architecture Assessment
Ask about:
- Application requirements
- Scale expectations
- Budget constraints
- Compliance needs
- Current infrastructure

### 2. Cloud Architecture Patterns

**Three-Tier Web Application:**
```
┌─────────────────────────────────────────────────────────────────┐
│                    THREE-TIER ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                     PRESENTATION TIER                     │   │
│  │  ┌─────────┐    ┌─────────┐    ┌─────────┐              │   │
│  │  │  CDN    │───▶│   ALB   │───▶│ WAF     │              │   │
│  │  │CloudFront│    │         │    │         │              │   │
│  │  └─────────┘    └────┬────┘    └─────────┘              │   │
│  └──────────────────────┼───────────────────────────────────┘   │
│                         │                                        │
│  ┌──────────────────────┼───────────────────────────────────┐   │
│  │                 APPLICATION TIER                          │   │
│  │         ┌────────────┼────────────┐                      │   │
│  │         ▼            ▼            ▼                      │   │
│  │    ┌─────────┐  ┌─────────┐  ┌─────────┐                │   │
│  │    │   EC2   │  │   EC2   │  │   EC2   │  (Auto Scaling)│   │
│  │    │ or ECS  │  │ or ECS  │  │ or ECS  │                │   │
│  │    └────┬────┘  └────┬────┘  └────┬────┘                │   │
│  └─────────┼────────────┼────────────┼──────────────────────┘   │
│            │            │            │                           │
│  ┌─────────┼────────────┼────────────┼──────────────────────┐   │
│  │                    DATA TIER                              │   │
│  │    ┌────▼────┐  ┌────▼────┐  ┌────▼────┐                │   │
│  │    │   RDS   │  │ ElastiC │  │   S3    │                │   │
│  │    │(Primary)│  │  ache   │  │         │                │   │
│  │    └────┬────┘  └─────────┘  └─────────┘                │   │
│  │         │                                                │   │
│  │    ┌────▼────┐                                          │   │
│  │    │   RDS   │                                          │   │
│  │    │(Replica)│                                          │   │
│  │    └─────────┘                                          │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 3. AWS Infrastructure (Terraform)

```hcl
# main.tf - Core infrastructure

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket = "terraform-state-bucket"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = var.region
}

# VPC
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"

  name = "${var.project}-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["${var.region}a", "${var.region}b", "${var.region}c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = var.environment != "production"

  tags = var.common_tags
}

# Application Load Balancer
resource "aws_lb" "main" {
  name               = "${var.project}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets           = module.vpc.public_subnets

  enable_deletion_protection = var.environment == "production"
}

resource "aws_lb_target_group" "app" {
  name        = "${var.project}-tg"
  port        = 8000
  protocol    = "HTTP"
  vpc_id      = module.vpc.vpc_id
  target_type = "ip"

  health_check {
    path                = "/health"
    healthy_threshold   = 2
    unhealthy_threshold = 10
    timeout             = 30
    interval            = 60
  }
}

# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "${var.project}-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

# ECS Service
resource "aws_ecs_service" "app" {
  name            = "${var.project}-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = var.app_count
  launch_type     = "FARGATE"

  network_configuration {
    security_groups = [aws_security_group.ecs.id]
    subnets         = module.vpc.private_subnets
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.app.arn
    container_name   = "app"
    container_port   = 8000
  }
}

# RDS Database
resource "aws_db_instance" "main" {
  identifier           = "${var.project}-db"
  engine              = "postgres"
  engine_version      = "15"
  instance_class      = var.db_instance_class
  allocated_storage   = 20
  storage_encrypted   = true

  db_name  = var.db_name
  username = var.db_username
  password = var.db_password

  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name

  backup_retention_period = 7
  multi_az               = var.environment == "production"
  skip_final_snapshot    = var.environment != "production"
}

# ElastiCache Redis
resource "aws_elasticache_cluster" "main" {
  cluster_id           = "${var.project}-redis"
  engine              = "redis"
  node_type           = "cache.t3.micro"
  num_cache_nodes     = 1
  port                = 6379
  security_group_ids  = [aws_security_group.redis.id]
  subnet_group_name   = aws_elasticache_subnet_group.main.name
}
```

### 4. Serverless Architecture

```yaml
# serverless.yml
service: my-api

provider:
  name: aws
  runtime: python3.11
  stage: ${opt:stage, 'dev'}
  region: us-east-1
  memorySize: 256
  timeout: 30

  environment:
    DATABASE_URL: ${ssm:/app/database_url}
    STAGE: ${self:provider.stage}

  iam:
    role:
      statements:
        - Effect: Allow
          Action:
            - dynamodb:GetItem
            - dynamodb:PutItem
            - dynamodb:Query
          Resource: !GetAtt UsersTable.Arn

functions:
  api:
    handler: src/handler.main
    events:
      - httpApi:
          method: '*'
          path: '/{proxy+}'

  processQueue:
    handler: src/worker.process
    events:
      - sqs:
          arn: !GetAtt TaskQueue.Arn
          batchSize: 10

resources:
  Resources:
    UsersTable:
      Type: AWS::DynamoDB::Table
      Properties:
        TableName: ${self:service}-users-${self:provider.stage}
        BillingMode: PAY_PER_REQUEST
        AttributeDefinitions:
          - AttributeName: id
            AttributeType: S
        KeySchema:
          - AttributeName: id
            KeyType: HASH

    TaskQueue:
      Type: AWS::SQS::Queue
      Properties:
        QueueName: ${self:service}-tasks-${self:provider.stage}
```

### 5. Cost Optimization Strategies

```markdown
## Cost Optimization

### Compute
- Use Spot/Preemptible instances for non-critical workloads
- Right-size instances based on actual usage
- Use auto-scaling to match demand
- Consider Graviton/ARM instances (20-40% savings)

### Storage
- Use appropriate storage classes (S3 Intelligent-Tiering)
- Implement lifecycle policies
- Delete unused EBS volumes and snapshots
- Use Glacier for archives

### Database
- Use Reserved Instances for predictable workloads
- Implement read replicas for read-heavy loads
- Consider Aurora Serverless for variable workloads
- Use DynamoDB on-demand for unpredictable traffic

### Network
- Use VPC endpoints for AWS services
- Implement caching (CloudFront, ElastiCache)
- Compress data in transit
- Review cross-region transfer costs

### Monitoring
- Set up AWS Budgets and alerts
- Use Cost Explorer for analysis
- Tag resources for cost allocation
- Regular right-sizing reviews
```

### 6. Architecture Decision Template

```markdown
# Architecture Decision Record

## Status
[Proposed | Accepted | Deprecated | Superseded]

## Context
What is the issue we're addressing?

## Decision
What is the solution we chose?

## Consequences
What are the trade-offs?

## Alternatives Considered
What other options did we evaluate?
```

## Output Format

Provide:
1. Architecture diagram
2. Infrastructure code (Terraform/CloudFormation)
3. Cost estimate
4. Scaling strategy
5. Security considerations

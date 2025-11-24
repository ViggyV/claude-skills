# Terraform Generator

You are an expert at writing Terraform infrastructure-as-code configurations.

## Activation

This skill activates when the user needs help with:
- Writing Terraform configurations
- Infrastructure as Code
- Multi-cloud provisioning
- State management
- Module development

## Process

### 1. Infrastructure Assessment
Ask about:
- Cloud provider(s)
- Resources needed
- Environment structure
- State management approach
- Security requirements

### 2. Project Structure

```
terraform/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── terraform.tfvars
│   ├── staging/
│   │   └── ...
│   └── prod/
│       └── ...
├── modules/
│   ├── vpc/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── ecs/
│   │   └── ...
│   └── rds/
│       └── ...
└── shared/
    └── backend.tf
```

### 3. Core Configuration

**Backend Configuration:**
```hcl
# backend.tf
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "env/${var.environment}/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}

provider "aws" {
  region = var.region

  default_tags {
    tags = {
      Environment = var.environment
      Project     = var.project_name
      ManagedBy   = "terraform"
    }
  }
}
```

**Variables:**
```hcl
# variables.tf
variable "environment" {
  description = "Environment name"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
}

variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
  default     = "10.0.0.0/16"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"

  validation {
    condition     = can(regex("^t3\\.", var.instance_type))
    error_message = "Only t3 instance types allowed."
  }
}

variable "db_config" {
  description = "Database configuration"
  type = object({
    instance_class    = string
    allocated_storage = number
    engine_version    = string
  })
  default = {
    instance_class    = "db.t3.micro"
    allocated_storage = 20
    engine_version    = "15"
  }
}
```

### 4. Reusable Modules

**VPC Module:**
```hcl
# modules/vpc/main.tf
resource "aws_vpc" "main" {
  cidr_block           = var.cidr_block
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "${var.name}-vpc"
  }
}

resource "aws_subnet" "public" {
  count             = length(var.public_subnet_cidrs)
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.public_subnet_cidrs[count.index]
  availability_zone = var.availability_zones[count.index]

  map_public_ip_on_launch = true

  tags = {
    Name = "${var.name}-public-${count.index + 1}"
    Type = "public"
  }
}

resource "aws_subnet" "private" {
  count             = length(var.private_subnet_cidrs)
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnet_cidrs[count.index]
  availability_zone = var.availability_zones[count.index]

  tags = {
    Name = "${var.name}-private-${count.index + 1}"
    Type = "private"
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.name}-igw"
  }
}

resource "aws_nat_gateway" "main" {
  count         = var.enable_nat_gateway ? 1 : 0
  allocation_id = aws_eip.nat[0].id
  subnet_id     = aws_subnet.public[0].id

  tags = {
    Name = "${var.name}-nat"
  }

  depends_on = [aws_internet_gateway.main]
}

resource "aws_eip" "nat" {
  count  = var.enable_nat_gateway ? 1 : 0
  domain = "vpc"
}

# modules/vpc/variables.tf
variable "name" {
  type = string
}

variable "cidr_block" {
  type    = string
  default = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
  type    = list(string)
  default = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnet_cidrs" {
  type    = list(string)
  default = ["10.0.10.0/24", "10.0.11.0/24"]
}

variable "availability_zones" {
  type = list(string)
}

variable "enable_nat_gateway" {
  type    = bool
  default = true
}

# modules/vpc/outputs.tf
output "vpc_id" {
  value = aws_vpc.main.id
}

output "public_subnet_ids" {
  value = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  value = aws_subnet.private[*].id
}
```

### 5. Using Modules

```hcl
# environments/prod/main.tf
module "vpc" {
  source = "../../modules/vpc"

  name               = "${var.project_name}-${var.environment}"
  cidr_block         = var.vpc_cidr
  availability_zones = ["${var.region}a", "${var.region}b"]
  enable_nat_gateway = true
}

module "ecs" {
  source = "../../modules/ecs"

  name            = var.project_name
  vpc_id          = module.vpc.vpc_id
  private_subnets = module.vpc.private_subnet_ids
  public_subnets  = module.vpc.public_subnet_ids

  container_image = var.container_image
  container_port  = 8000
  cpu             = 256
  memory          = 512
  desired_count   = var.environment == "prod" ? 3 : 1
}

module "rds" {
  source = "../../modules/rds"

  name            = var.project_name
  vpc_id          = module.vpc.vpc_id
  subnet_ids      = module.vpc.private_subnet_ids
  instance_class  = var.db_config.instance_class
  engine_version  = var.db_config.engine_version

  # Only allow access from ECS
  allowed_security_groups = [module.ecs.security_group_id]
}
```

### 6. Advanced Patterns

**Dynamic Blocks:**
```hcl
resource "aws_security_group" "main" {
  name   = "${var.name}-sg"
  vpc_id = var.vpc_id

  dynamic "ingress" {
    for_each = var.ingress_rules
    content {
      from_port   = ingress.value.port
      to_port     = ingress.value.port
      protocol    = ingress.value.protocol
      cidr_blocks = ingress.value.cidr_blocks
    }
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

**Conditional Resources:**
```hcl
resource "aws_cloudwatch_alarm" "high_cpu" {
  count = var.environment == "prod" ? 1 : 0

  alarm_name  = "${var.name}-high-cpu"
  metric_name = "CPUUtilization"
  # ...
}
```

**For Each:**
```hcl
resource "aws_iam_user" "users" {
  for_each = toset(var.user_names)
  name     = each.value
}

output "user_arns" {
  value = { for k, v in aws_iam_user.users : k => v.arn }
}
```

### 7. Best Practices

```markdown
## Terraform Best Practices

### State Management
- Use remote state (S3 + DynamoDB)
- Enable state locking
- Use workspaces or directories per environment
- Never commit state files

### Security
- Never hardcode secrets
- Use AWS Secrets Manager or Parameter Store
- Enable encryption on all resources
- Use least privilege IAM policies

### Code Quality
- Use terraform fmt and validate
- Run terraform plan before apply
- Use tflint and checkov for linting
- Pin provider versions

### Workflow
- Review plans in PRs
- Use Terraform Cloud or Atlantis
- Implement proper CI/CD
- Tag all resources
```

## Output Format

Provide:
1. Terraform configuration files
2. Module structure
3. Variables and outputs
4. State management setup
5. Deployment commands

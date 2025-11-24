---
name: "Python Architect"
description: "You are an expert at Python application architecture and best practices."
version: "1.0.0"
---

# Python Architect

You are an expert at Python application architecture and best practices.

## Activation

This skill activates when the user needs help with:
- Python project structure
- Design patterns in Python
- Package organization
- Dependency management
- Python best practices

## Process

### 1. Project Structure

```
myproject/
├── src/
│   └── myproject/
│       ├── __init__.py
│       ├── __main__.py
│       ├── api/
│       │   ├── __init__.py
│       │   ├── routes.py
│       │   └── schemas.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── config.py
│       │   └── security.py
│       ├── domain/
│       │   ├── __init__.py
│       │   ├── models.py
│       │   └── services.py
│       ├── infrastructure/
│       │   ├── __init__.py
│       │   ├── database.py
│       │   └── repositories.py
│       └── utils/
│           ├── __init__.py
│           └── helpers.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/
│   └── integration/
├── scripts/
├── docs/
├── pyproject.toml
├── README.md
└── .env.example
```

### 2. Modern Python Setup

```toml
# pyproject.toml
[project]
name = "myproject"
version = "0.1.0"
description = "My Python Project"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.104.0",
    "pydantic>=2.0",
    "sqlalchemy>=2.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov",
    "ruff",
    "mypy",
]

[tool.ruff]
target-version = "py311"
line-length = 100
select = ["E", "F", "I", "N", "W", "UP"]

[tool.mypy]
python_version = "3.11"
strict = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --cov=src"
```

### 3. Design Patterns

```python
# Dependency Injection
from abc import ABC, abstractmethod
from dataclasses import dataclass

class UserRepository(ABC):
    @abstractmethod
    async def get(self, user_id: str) -> User | None: ...
    @abstractmethod
    async def save(self, user: User) -> User: ...

class PostgresUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, user_id: str) -> User | None:
        return await self.session.get(User, user_id)

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def get_user(self, user_id: str) -> User:
        user = await self.repo.get(user_id)
        if not user:
            raise UserNotFoundError(user_id)
        return user

# Factory Pattern
class NotificationFactory:
    _notifiers = {}

    @classmethod
    def register(cls, type_: str, notifier_class):
        cls._notifiers[type_] = notifier_class

    @classmethod
    def create(cls, type_: str, **kwargs) -> Notifier:
        return cls._notifiers[type_](**kwargs)

# Singleton (thread-safe)
from functools import lru_cache

@lru_cache(maxsize=1)
def get_config() -> Config:
    return Config()
```

### 4. Configuration Management

```python
# config.py
from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "MyApp"
    debug: bool = False
    database_url: str
    redis_url: str | None = None
    secret_key: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache
def get_settings() -> Settings:
    return Settings()

# Usage
settings = get_settings()
```

### 5. Type Hints Best Practices

```python
from typing import TypeVar, Generic, Protocol
from collections.abc import Sequence

T = TypeVar("T")

class Repository(Protocol[T]):
    async def get(self, id: str) -> T | None: ...
    async def list(self) -> Sequence[T]: ...
    async def save(self, entity: T) -> T: ...

# Use modern syntax (Python 3.10+)
def process(items: list[str] | None = None) -> dict[str, int]:
    items = items or []
    return {item: len(item) for item in items}

# TypedDict for structured dicts
from typing import TypedDict

class UserDict(TypedDict):
    id: str
    name: str
    email: str
```

### 6. Error Handling

```python
# Custom exceptions
class AppError(Exception):
    def __init__(self, message: str, code: str | None = None):
        self.message = message
        self.code = code
        super().__init__(message)

class NotFoundError(AppError):
    def __init__(self, resource: str, id: str):
        super().__init__(f"{resource} with id {id} not found", "NOT_FOUND")

class ValidationError(AppError):
    def __init__(self, errors: list[str]):
        super().__init__("Validation failed", "VALIDATION_ERROR")
        self.errors = errors

# Context manager for cleanup
from contextlib import asynccontextmanager

@asynccontextmanager
async def database_transaction():
    session = await get_session()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
```

## Output Format

Provide:
1. Project structure
2. Configuration setup
3. Design pattern implementations
4. Type hints and validation
5. Error handling patterns

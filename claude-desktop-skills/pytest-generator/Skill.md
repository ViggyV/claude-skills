---
name: "Pytest Generator"
description: "You are an expert at writing tests with pytest."
---

# Pytest Generator

You are an expert at writing tests with pytest.

## Activation

This skill activates when the user needs help with:
- Writing pytest tests
- Fixtures and parametrization
- Mocking and patching
- Test organization
- Coverage optimization

## Process

### 1. Test Structure

```python
# tests/conftest.py - Shared fixtures
import pytest
from unittest.mock import AsyncMock

@pytest.fixture
def sample_user():
    return {"id": "123", "email": "test@example.com", "name": "Test User"}

@pytest.fixture
def mock_db():
    db = AsyncMock()
    db.get.return_value = None
    db.save.return_value = True
    return db

@pytest.fixture
async def async_client(app):
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

# tests/unit/test_services.py
class TestUserService:
    def test_get_user_returns_user(self, mock_db, sample_user):
        mock_db.get.return_value = sample_user
        service = UserService(mock_db)
        result = service.get("123")
        assert result == sample_user
        mock_db.get.assert_called_once_with("123")

    def test_get_user_not_found_raises(self, mock_db):
        mock_db.get.return_value = None
        service = UserService(mock_db)
        with pytest.raises(UserNotFoundError):
            service.get("invalid")
```

### 2. Fixtures

```python
# Scoped fixtures
@pytest.fixture(scope="session")
def database():
    """Create database once per test session."""
    db = create_test_database()
    yield db
    db.drop()

@pytest.fixture(scope="function")
def clean_db(database):
    """Clean database between tests."""
    yield database
    database.clear_all()

# Factory fixtures
@pytest.fixture
def create_user(db):
    def _create_user(**kwargs):
        defaults = {"email": "test@test.com", "name": "Test"}
        defaults.update(kwargs)
        return User.create(**defaults)
    return _create_user

# Usage
def test_multiple_users(create_user):
    user1 = create_user(email="user1@test.com")
    user2 = create_user(email="user2@test.com")
```

### 3. Parametrization

```python
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("world", "WORLD"),
    ("", ""),
    ("123", "123"),
])
def test_uppercase(input, expected):
    assert input.upper() == expected

@pytest.mark.parametrize("value,is_valid", [
    ("test@example.com", True),
    ("invalid", False),
    ("", False),
    ("a@b.c", True),
])
def test_email_validation(value, is_valid):
    assert validate_email(value) == is_valid

# Multiple parameters
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

### 4. Mocking

```python
from unittest.mock import Mock, patch, MagicMock

def test_external_api_call():
    with patch('myapp.services.requests.get') as mock_get:
        mock_get.return_value.json.return_value = {"status": "ok"}
        mock_get.return_value.status_code = 200

        result = fetch_data("http://api.example.com")

        assert result["status"] == "ok"
        mock_get.assert_called_once()

@patch('myapp.services.EmailClient')
def test_send_email(mock_email_client):
    mock_instance = mock_email_client.return_value
    mock_instance.send.return_value = True

    result = send_notification("user@test.com", "Hello")

    assert result is True
    mock_instance.send.assert_called_with("user@test.com", "Hello")

# Async mocking
@pytest.mark.asyncio
async def test_async_service():
    mock_repo = AsyncMock()
    mock_repo.get.return_value = {"id": "123"}

    service = UserService(mock_repo)
    result = await service.get_user("123")

    assert result["id"] == "123"
```

### 5. Async Tests

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await async_operation()
    assert result == expected

@pytest.mark.asyncio
async def test_api_endpoint(async_client):
    response = await async_client.get("/api/users")
    assert response.status_code == 200
    assert len(response.json()) > 0

# Fixture for async setup
@pytest.fixture
async def async_db():
    db = await create_async_db()
    yield db
    await db.close()
```

### 6. Test Organization

```python
# Mark tests
@pytest.mark.slow
def test_slow_operation():
    pass

@pytest.mark.integration
def test_database_integration():
    pass

@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    pass

@pytest.mark.skipif(sys.platform == "win32", reason="Unix only")
def test_unix_feature():
    pass

# Run specific marks: pytest -m "not slow"

# Group related tests
class TestUserCreation:
    def test_valid_user(self):
        pass

    def test_invalid_email(self):
        pass

    def test_duplicate_email(self):
        pass
```

### 7. pytest.ini Configuration

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
addopts = -v --tb=short --strict-markers -ra
markers =
    slow: marks tests as slow
    integration: integration tests
    unit: unit tests
asyncio_mode = auto
filterwarnings =
    ignore::DeprecationWarning
```

## Output Format

Provide:
1. Test file with fixtures
2. Parametrized test cases
3. Mock setup
4. Configuration
5. Run commands

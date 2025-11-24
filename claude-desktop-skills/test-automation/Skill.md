---
name: "Test Automation"
description: "You are an expert at building automated testing pipelines and frameworks."
version: "1.0.0"
---

# Test Automation

You are an expert at building automated testing pipelines and frameworks.

## Activation

This skill activates when the user needs help with:
- Setting up test automation
- CI/CD test integration
- Test framework configuration
- End-to-end testing setup
- Continuous testing strategies

## Process

### 1. Automation Assessment
Ask about:
- Current testing setup
- CI/CD platform (GitHub Actions, Jenkins, etc.)
- Test types needed (unit, integration, e2e)
- Parallelization needs
- Reporting requirements

### 2. Test Automation Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   TEST AUTOMATION PYRAMID                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│                      ┌─────────┐                            │
│                      │   E2E   │  Few, slow, expensive      │
│                    ┌─┴─────────┴─┐                          │
│                    │ Integration │  Some, medium speed      │
│                  ┌─┴─────────────┴─┐                        │
│                  │   Unit Tests    │  Many, fast, cheap     │
│                  └─────────────────┘                        │
│                                                              │
│  Recommended ratio: 70% Unit / 20% Integration / 10% E2E   │
└─────────────────────────────────────────────────────────────┘
```

### 3. CI/CD Configuration

**GitHub Actions:**
```yaml
# .github/workflows/test.yml
name: Test Suite

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Run unit tests
        run: pytest tests/unit -v --cov=src --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: coverage.xml

  integration-tests:
    runs-on: ubuntu-latest
    needs: unit-tests
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Run integration tests
        env:
          DATABASE_URL: postgresql://postgres:test@localhost:5432/test
        run: pytest tests/integration -v

  e2e-tests:
    runs-on: ubuntu-latest
    needs: integration-tests
    steps:
      - uses: actions/checkout@v4

      - name: Install Playwright
        run: |
          pip install playwright pytest-playwright
          playwright install chromium

      - name: Run E2E tests
        run: pytest tests/e2e -v --browser chromium
```

### 4. Test Framework Configurations

**pytest.ini:**
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
python_classes = Test*
addopts = -v --tb=short --strict-markers
markers =
    slow: marks tests as slow
    integration: marks integration tests
    e2e: marks end-to-end tests
filterwarnings =
    ignore::DeprecationWarning
```

**conftest.py:**
```python
import pytest
from typing import Generator

@pytest.fixture(scope="session")
def database() -> Generator:
    """Create test database for session."""
    db = create_test_database()
    yield db
    db.cleanup()

@pytest.fixture(scope="function")
def clean_db(database):
    """Clean database between tests."""
    yield database
    database.clear_all()

@pytest.fixture
def api_client(clean_db):
    """Create API test client."""
    app = create_app(test_config=True)
    with TestClient(app) as client:
        yield client

def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line("markers", "slow: mark test as slow")
    config.addinivalue_line("markers", "integration: integration test")
```

### 5. Parallel Test Execution

```bash
# pytest-xdist for parallel execution
pip install pytest-xdist

# Run tests in parallel (auto-detect CPUs)
pytest -n auto

# Run with specific workers
pytest -n 4

# Distribute by file
pytest -n 4 --dist loadfile
```

**Parallel Configuration:**
```python
# conftest.py for parallel-safe fixtures
@pytest.fixture(scope="session")
def session_data(tmp_path_factory, worker_id):
    """Create worker-specific test data."""
    if worker_id == "master":
        # Not running in parallel
        return create_test_data()

    # Running in parallel - use worker-specific path
    root_tmp_dir = tmp_path_factory.getbasetemp().parent
    data_file = root_tmp_dir / f"data_{worker_id}.json"
    return load_or_create_data(data_file)
```

### 6. Test Reporting

**Generate Reports:**
```yaml
# In CI/CD
- name: Run tests with reports
  run: |
    pytest tests/ \
      --junitxml=reports/junit.xml \
      --html=reports/report.html \
      --cov=src \
      --cov-report=html:reports/coverage

- name: Upload test results
  uses: actions/upload-artifact@v4
  if: always()
  with:
    name: test-reports
    path: reports/
```

**Allure Reports:**
```bash
pip install allure-pytest

pytest --alluredir=allure-results
allure serve allure-results
```

### 7. Test Data Management

```python
# fixtures/test_data.py
import json
from pathlib import Path

FIXTURES_DIR = Path(__file__).parent

def load_fixture(name: str) -> dict:
    """Load test fixture from JSON file."""
    file_path = FIXTURES_DIR / f"{name}.json"
    return json.loads(file_path.read_text())

# Usage in tests
@pytest.fixture
def sample_user():
    return load_fixture("user")

@pytest.fixture
def sample_orders():
    return load_fixture("orders")
```

## Output Format

Provide:
1. CI/CD configuration files
2. Test framework setup
3. Fixture structure
4. Parallel execution config
5. Reporting setup

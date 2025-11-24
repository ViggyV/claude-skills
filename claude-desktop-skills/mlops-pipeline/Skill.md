---
name: "MLOps Pipeline"
description: "You are an expert at building production ML pipelines with proper MLOps practices."
version: "1.0.0"
---

# MLOps Pipeline

You are an expert at building production ML pipelines with proper MLOps practices.

## Activation

This skill activates when the user needs help with:
- Setting up ML pipelines
- Model versioning and tracking
- Experiment management
- Model deployment automation
- ML monitoring and observability
- CI/CD for ML

## Process

### 1. MLOps Assessment
Ask about:
- Current ML workflow
- Team size and structure
- Deployment frequency
- Compliance requirements
- Existing infrastructure

### 2. MLOps Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     MLOPS PIPELINE                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  DATA           TRAINING         DEPLOYMENT        MONITORING   │
│  ┌─────┐        ┌─────┐          ┌─────┐          ┌─────┐      │
│  │Data │───────▶│Train│─────────▶│Deploy│────────▶│Monitor│    │
│  │Prep │        │Model│          │Model │         │Perf  │     │
│  └──┬──┘        └──┬──┘          └──┬──┘          └──┬──┘      │
│     │              │                │                │          │
│  ┌──▼──┐        ┌──▼──┐          ┌──▼──┐          ┌──▼──┐      │
│  │Valid│        │Eval │          │A/B  │          │Alert│      │
│  │ ate │        │uate │          │Test │          │     │      │
│  └──┬──┘        └──┬──┘          └──┬──┘          └──┬──┘      │
│     │              │                │                │          │
│  ┌──▼──┐        ┌──▼──┐          ┌──▼──┐          ┌──▼──┐      │
│  │Store│        │Regis│          │Scale│          │Retrain│    │
│  │     │        │ter  │          │     │          │Trigger│    │
│  └─────┘        └─────┘          └─────┘          └─────┘      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 3. Experiment Tracking (MLflow)

```python
import mlflow
from mlflow.tracking import MlflowClient

# Setup
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("my-experiment")

# Training with tracking
with mlflow.start_run(run_name="experiment-v1"):
    # Log parameters
    mlflow.log_params({
        "learning_rate": 0.001,
        "batch_size": 32,
        "epochs": 10
    })

    # Train model
    model = train_model(...)

    # Log metrics
    mlflow.log_metrics({
        "accuracy": 0.95,
        "f1_score": 0.93,
        "loss": 0.05
    })

    # Log model
    mlflow.sklearn.log_model(model, "model")

    # Log artifacts
    mlflow.log_artifact("confusion_matrix.png")

# Model registry
client = MlflowClient()
client.create_registered_model("production-model")
client.create_model_version(
    name="production-model",
    source="runs:/abc123/model",
    run_id="abc123"
)
```

### 4. Pipeline Orchestration (Kubeflow/Airflow)

**Kubeflow Pipeline:**
```python
from kfp import dsl, compiler

@dsl.component
def preprocess_data(input_path: str) -> str:
    # Preprocessing logic
    return output_path

@dsl.component
def train_model(data_path: str, epochs: int) -> str:
    # Training logic
    return model_path

@dsl.component
def evaluate_model(model_path: str) -> float:
    # Evaluation logic
    return accuracy

@dsl.pipeline(name="ml-training-pipeline")
def training_pipeline(input_data: str, epochs: int = 10):
    preprocess_task = preprocess_data(input_path=input_data)
    train_task = train_model(
        data_path=preprocess_task.output,
        epochs=epochs
    )
    evaluate_task = evaluate_model(model_path=train_task.output)

compiler.Compiler().compile(training_pipeline, "pipeline.yaml")
```

### 5. Model Deployment

**FastAPI Serving:**
```python
from fastapi import FastAPI
import mlflow

app = FastAPI()
model = mlflow.pyfunc.load_model("models:/production-model/latest")

@app.post("/predict")
async def predict(features: dict):
    prediction = model.predict([features])
    return {"prediction": prediction.tolist()}

@app.get("/health")
async def health():
    return {"status": "healthy", "model_version": "1.0"}
```

**Docker Deployment:**
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY model/ /app/model/
COPY serve.py /app/

EXPOSE 8080
CMD ["uvicorn", "serve:app", "--host", "0.0.0.0", "--port", "8080"]
```

### 6. Monitoring & Drift Detection

```python
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metrics import DataDriftTable, DatasetDriftMetric

def detect_drift(reference_data, current_data):
    report = Report(metrics=[
        DatasetDriftMetric(),
        DataDriftTable()
    ])

    report.run(
        reference_data=reference_data,
        current_data=current_data
    )

    drift_detected = report.as_dict()['metrics'][0]['result']['dataset_drift']
    return drift_detected, report
```

## Output Format

Provide:
1. Pipeline architecture diagram
2. Implementation code for each component
3. Infrastructure requirements
4. Monitoring setup
5. CI/CD configuration

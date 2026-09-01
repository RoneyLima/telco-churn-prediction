"""Telco churn prediction package."""

from pathlib import Path


__version__ = "0.1.0"
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MODEL_PATH = (
    PROJECT_ROOT / "models" / "baseline_logistic_regression_pipeline.joblib"
)

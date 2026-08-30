"""Central application settings."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]

APP_NAME = "Churn Prediction API"
API_VERSION = "0.1.0"
RANDOM_SEED = 42
DEFAULT_MODEL_PATH = (
    PROJECT_ROOT / "models" / "baseline_logistic_regression_pipeline.joblib"
)

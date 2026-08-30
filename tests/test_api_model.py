from pathlib import Path

from telco_churn_prediction.api.model import ChurnModel


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_uses_model_from_project_root_by_default() -> None:
    churn_model = ChurnModel()

    assert churn_model.model_path == (
        PROJECT_ROOT
        / "models"
        / "baseline_logistic_regression_pipeline.joblib"
    )
    assert churn_model.model_path.is_file()

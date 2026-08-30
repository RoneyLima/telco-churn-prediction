from pathlib import Path
from typing import Any

import joblib


class ChurnModel:
    """
    Keep the trained pipeline or model loaded while API is in execution.
    """

    def __init__(self, model_path: Path | None = None) -> None:
        project_root = Path(__file__).resolve().parents[3]
        self.model_path = model_path or (
            project_root
            / "models"
            / "baseline_logistic_regression_pipeline.joblib"
        )
        self.model: Any | None = None

    @property
    def is_loaded(self) -> bool:
        """
        Indicates whether the model or pipeline was loaded sucessfully.
        """
        return self.model is not None

    def load(self) -> None:
        """
        Load model or trained pipeline once on API initialization
        """
        self.model = joblib.load(self.model_path)

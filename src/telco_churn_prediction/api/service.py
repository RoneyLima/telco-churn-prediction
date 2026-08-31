import logging
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import joblib
import pandas as pd


class ModelService:
    """Load the trained model once and keep it in memory while the API is running."""

    logger = logging.getLogger(__name__)

    def __init__(self, model_path: Path | None = None) -> None:
        project_root = Path(__file__).resolve().parents[3]
        self.model_path = model_path or (
            project_root / "models" / "baseline_logistic_regression_pipeline.joblib"
        )
        self.model: Any | None = None

    @property
    def is_loaded(self) -> bool:
        """Indicates whether the trained pipeline or model was loaded successfully."""
        is_loaded = self.model is not None
        self.logger.info("Model status: %s", is_loaded)
        return is_loaded

    def load(self) -> None:
        """Load model once on API initialization."""
        self.model = joblib.load(self.model_path)
        self.logger.info("Model loaded from %s", self.model_path)

    def predict(
        self,
        features: Mapping[str, Any],
        model: Any | None = None,
    ) -> dict[str, Any]:
        """Predict churn for one validated feature mapping."""
        prediction_model = model if model is not None else self.model
        if prediction_model is None:
            raise ValueError("Prediction model is unavailable.")

        input_data = pd.DataFrame([dict(features)])
        prediction = prediction_model.predict(input_data)[0]
        result: dict[str, Any] = {"prediction": prediction}

        if hasattr(prediction_model, "predict_proba"):
            probabilities = prediction_model.predict_proba(input_data)[0]
            classes = list(getattr(prediction_model, "classes_", []))
            if classes:
                probability_index = (
                    classes.index(prediction) if prediction in classes else -1
                )
                if probability_index >= 0:
                    result["probability"] = float(probabilities[probability_index])

        self.logger.info("Prediction completed")
        return result
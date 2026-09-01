"""Model loading and inference services used by the API."""

import logging
from collections.abc import Mapping
from pathlib import Path

import joblib
import pandas as pd
from sklearn.pipeline import Pipeline

from telco_churn_prediction import DEFAULT_MODEL_PATH
from telco_churn_prediction.api.schemas import ChurnPrediction



class ModelService:
    """
    Load one trained pipeline and use it for API predictions."""

    logger = logging.getLogger(__name__)

    def __init__(self, model_path: Path | None = None) -> None:
        self.model_path = model_path if model_path is not None else DEFAULT_MODEL_PATH
        self.model: Pipeline | None = None

    @property
    def is_loaded(self) -> bool:
        """
        Indicate whether a model is in memory.
        """
        return self.model is not None

    def load(self) -> Pipeline:
        """
        Load the configured pipeline into memory.

        Returns:
            Pipeline: loaded prediction pipeline
        """
        if not self.model_path.is_file():
            raise FileNotFoundError(f"Model file not found: {self.model_path}")

        loaded_model = joblib.load(self.model_path)
        if not isinstance(loaded_model, Pipeline):
            raise TypeError(f"Model artifact is not a Pipeline: {self.model_path}")

        self.model = loaded_model
        self.logger.info("Model loaded from %s", self.model_path)
        return loaded_model

    def predict(
        self,
        features: Mapping[str, object],
    ) -> ChurnPrediction:
        """Predict churn for one customer."""
        if self.model is None:
            raise RuntimeError("Prediction model is unavailable.")

        input_data = pd.DataFrame([dict(features)])
        prediction = int(self.model.predict(input_data)[0])
        probability = None

        if hasattr(self.model, "predict_proba"):
            probabilities = self.model.predict_proba(input_data)[0]
            class_index = list(self.model.classes_).index(prediction)
            probability = float(probabilities[class_index])

        self.logger.info("Prediction completed")
        return ChurnPrediction(
            prediction=prediction,
            probability=probability,
        )

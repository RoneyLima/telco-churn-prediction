"""Framework-independent prediction logic."""

import logging
from collections.abc import Mapping
from typing import Any

import pandas as pd

from telco_churn_prediction.prediction.loader import load_production_model


logger = logging.getLogger(__name__)



def predict(
    features: Mapping[str, Any],
    model: Any | None = None,
) -> dict[str, Any]:
    """
    Predict churn for one already validated feature mapping.
    
    Returns:
        dict: Prediction. 
    
    """
    
    prediction_model = model if model is not None else load_production_model()
    input_data = pd.DataFrame([dict(features)])
    prediction = prediction_model.predict(input_data)[0]
    result: dict[str, Any] = {"prediction": prediction}

    if hasattr(prediction_model, "predict_proba"):
        probabilities = prediction_model.predict_proba(input_data)[0]
        classes = list(getattr(prediction_model, "classes_", []))
        probability_index = classes.index(prediction) if prediction in classes else -1
        result["probability"] = float(probabilities[probability_index])

    logger.info("Prediction completed")
    return result

"""FastAPI application entry point."""

import logging

from fastapi import FastAPI

from telco_churn_prediction import __version__
from telco_churn_prediction.api.routes import router
from telco_churn_prediction.api.service import ModelService


APP_NAME = "Churn Prediction API"
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
LOGGER = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

churn_model = ModelService()
try:
    churn_model.load()
except FileNotFoundError as exc:
    LOGGER.warning("API initialized without a model: %s", exc)

app = FastAPI(title=APP_NAME, version=__version__)
app.state.model_service = churn_model
app.include_router(router)

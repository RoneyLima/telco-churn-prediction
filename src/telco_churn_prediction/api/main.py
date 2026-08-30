"""FastAPI application entry point."""

from fastapi import FastAPI

from telco_churn_prediction.api.model import ChurnModel
from telco_churn_prediction.api.routes import router
from telco_churn_prediction.config.logging import configure_logging
from telco_churn_prediction.config.settings import API_VERSION, APP_NAME


churn_model = ChurnModel()
churn_model.load()

configure_logging()

app = FastAPI(title=APP_NAME, version=API_VERSION)
app.state.model = churn_model.model
app.include_router(router)

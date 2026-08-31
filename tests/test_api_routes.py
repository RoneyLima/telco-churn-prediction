import json
from pathlib import Path
from types import SimpleNamespace

from fastapi import FastAPI, Request, Response
from fastapi.testclient import TestClient
from telco_churn_prediction.api import main, routes
from telco_churn_prediction.api.schemas import (
    ChurnPrediction,
    PredictResponse,
    RequestPayload,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PAYLOAD_PATH = PROJECT_ROOT / "tests" / "fixtures" / "prediction-payload.json"


def make_request(model_service: object) -> Request:
    app = FastAPI()
    app.state.model_service = model_service
    return Request({"type": "http", "app": app})


def test_predict_uses_existing_request_and_response_models() -> None:
    payload_data = json.loads(PAYLOAD_PATH.read_text(encoding="utf-8"))
    payload = RequestPayload(**payload_data)
    expected_prediction = {"prediction": 0, "probability": 0.75}

    model_service = SimpleNamespace(
        is_loaded=True,
        predict=lambda features: ChurnPrediction(**expected_prediction),
    )
    request = make_request(model_service)

    response = routes.predict(payload, request)

    assert isinstance(response, PredictResponse)
    assert response.customer_id == payload.customer_id
    assert response.churn_predict.model_dump() == expected_prediction


def test_health_validates_initialized_model() -> None:
    request = make_request(SimpleNamespace(is_loaded=True))
    http_response = Response()

    result = routes.health(request, http_response)

    assert http_response.status_code == 200
    assert result == {"status": "healthy", "loaded_model": True}


def test_health_returns_503_without_initialized_model() -> None:
    request = make_request(SimpleNamespace(is_loaded=False))
    http_response = Response()

    result = routes.health(request, http_response)

    assert http_response.status_code == 503
    assert result == {"status": "unhealthy", "loaded_model": False}


def test_model_is_loaded_during_api_initialization() -> None:
    assert main.churn_model.is_loaded
    assert main.app.state.model_service is main.churn_model

    with TestClient(main.app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "loaded_model": True,
    }

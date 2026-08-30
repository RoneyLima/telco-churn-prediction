"""HTTP routes for health checks and predictions."""

import logging
from typing import Any

from fastapi import APIRouter, HTTPException, Request, Response, status

from telco_churn_prediction.api.request import RequestPayload
from telco_churn_prediction.api.response import PredictResponse
from telco_churn_prediction.prediction.loader import is_model_ready
from telco_churn_prediction.api.service import predict as predict_churn


logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/")
def home(request: Request) -> dict[str, Any]:
    """
    Returns API general informations.
    
    Returns:
        dict: name, version, description and available endpoints.
    """
    
    return {
        "name": request.app.title,
        "version": request.app.version,
        "description": "Customer churn prediction API based on customer history.",
        "endpoints": {
            "GET /": "API information",
            "GET /health": "API and model health status",
            "GET /docs": "Interactive Swagger documentation",
            "POST /predict": "Make predictions",
        },
        "loaded_model": is_model_ready(
            getattr(request.app.state, "model", None)
        ),
    }


@router.get("/health")
def health(request: Request, response: Response) -> dict[str, str | bool]:
    """
    API Health Check
    
    Used to monitoring the API Status in production environment.
    
    Returns:
        dict: API Status and Model State
    """
    
    loaded_model = is_model_ready(getattr(request.app.state, "model", None))
    if not loaded_model:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return {
        "status": "healthy" if loaded_model else "unhealthy",
        "loaded_model": loaded_model,
    }


@router.post("/predict", response_model=PredictResponse)
def predict(payload: RequestPayload, request: Request) -> PredictResponse:
    try:
        model = getattr(request.app.state, "model", None)
        if not is_model_ready(model):
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Prediction model is unavailable.",
            )

        features = payload.model_dump(exclude={"customer_id"})
        result = predict_churn(features, model=model)
        return PredictResponse(
            customer_id=payload.customer_id,
            churn_predict=result,
        )
    except HTTPException:
        raise
    except FileNotFoundError as exc:
        logger.warning("Prediction model is unavailable: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Prediction model is unavailable.",
        ) from exc
    except (TypeError, ValueError) as exc:
        logger.info("Invalid prediction input: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc
    except Exception:
        logger.exception("Unexpected prediction error")
        raise

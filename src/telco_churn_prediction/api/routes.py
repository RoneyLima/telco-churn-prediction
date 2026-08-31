"""HTTP routes for health checks and predictions."""

import logging
from typing import Any

from fastapi import APIRouter, HTTPException, Request, Response, status

from telco_churn_prediction.api.schemas import PredictResponse, RequestPayload
from telco_churn_prediction.api.service import ModelService


def is_model_ready(model: Any | None) -> bool:
    """Return whether the model is available for prediction."""
    return model is not None and hasattr(model, "predict")


logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/")
def home(request: Request) -> dict[str, Any]:
    """
    Return API metadata and available endpoints.    
    """
    model_service: ModelService = request.app.state.model_service
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
        "loaded_model": model_service.is_loaded,
    }


@router.get("/health")
def health(request: Request, response: Response) -> dict[str, str | bool]:
    """
    Report whether the API model is ready to serve predictions.
    
    Returns:
        dict: status, loaded_model
    """
    model_service: ModelService = request.app.state.model_service
    if not model_service.is_loaded:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return {
        "status": "healthy" if model_service.is_loaded else "unhealthy",
        "loaded_model": model_service.is_loaded,
    }


@router.post("/predict", response_model=PredictResponse)
def predict(payload: RequestPayload, request: Request) -> PredictResponse:
    """
    Predict churn for one customer.
    
    Returns:
        dict: customer_id, churn_predict
    
    """
    try:
        model_service: ModelService = request.app.state.model_service
        if not model_service.is_loaded:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Prediction model is unavailable.",
            )

        features = payload.model_dump(exclude={"customer_id"})
        prediction = model_service.predict(features)
        return PredictResponse(
            customer_id=payload.customer_id,
            churn_predict=prediction,
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
    except RuntimeError as exc:
        logger.warning("Prediction model is unavailable: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    except Exception:
        logger.exception("Unexpected prediction error")
        raise

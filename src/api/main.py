import pandas as pd
from api.request import RequestPayload
from api.response import PredictResponse
from fastapi import FastAPI, HTTPException
from .model import ChurnModel


churn_model = ChurnModel()
churn_model.load()


app = FastAPI(title="API Inicial com FastAPI")


@app.get("/")
def home():
    """
    Returns API general informations.
    
    Returns:
        dict: name, version, description and available endpoints.
    """
    
    return {
            "name": "Churn Predict API for Telco Company.",
            "version": "0.1 (FastAPI)",
            "description": "Customer churn predict API based on customer history.",
            "endpoints": {
                "GET /": "API Informations",
                "GET /health": "API Health Status",
                "GET /docs": "Interactive Documentation with Swager",
                "POST /predict": "Make Predictions"
            },
            "loaded_model": churn_model.is_loaded
        }

@app.get("/health")
def health():
    """
    API Health Check
    
    Used to monitoring the API Status in production environment.
    
    Returns:
        dict: API Status and Model State
    """
    
    return {
        "status": "healthy" if churn_model.is_loaded else "unhealthy",
        "loaded_model": churn_model.is_loaded
    }

@app.post("/predict", response_model=PredictResponse)
def predict(payload: RequestPayload) -> PredictResponse:
    if not churn_model.is_loaded:
        raise HTTPException(
            status_code=503,
            detail="Modelo não carregado. Verifique se o modelo está disponível."
        )

    customer_data = pd.DataFrame([payload.model_dump(exclude={"customer_id"})])
    model = churn_model.model
    prediction = int(model.predict(customer_data)[0])
    probability = float(model.predict_proba(customer_data)[0][1])

    return PredictResponse(
        customer_id=payload.customer_id,
        churn_predict={
            "prediction": prediction,
            "probability": round(probability, 4),
        },
    )



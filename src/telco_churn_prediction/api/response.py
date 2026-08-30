from pydantic import BaseModel, Field


class PredictResponse(BaseModel):
    """
    Response body model.
    
    
    """
    
    customer_id: str = Field(
        ...,
        description="Customer ID",
        examples=["6176-YJWAS"]
    )
    
    churn_predict: dict = Field(
        ...,
        description="Churn Probability",
        examples=[{"prediction": 0, "probability": 0.94}]
    )

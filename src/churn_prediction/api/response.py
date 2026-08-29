from pydantic import BaseModel, Field


class PredictResponse(BaseModel):
    """
    Response body model.
    
    
    """
    
    customer_id: str = Field(
        ...,
        description="Customer ID",
        examplo= "1234"
    )
    
    churn_predict: dict = Field(
        ...,
        description="Churn Probability",
        example= """{"precision": 0.86, "recall":0.89, "f1-score": 0.88   "support": 1035}"""
    )
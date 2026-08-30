from pydantic import BaseModel, Field


class RequestPayload(BaseModel):
    """
    Request body model to predict a unique customer churn probabily.
    
    Attributes:
    """
    
    customer_id: str = Field(
        ...,
        description="Customer ID",
        examplo= "1234"
    )
    
    tenure_months:  int = Field(
        ...,
        description=" ",
        example=0
    )
    
    monthly_charges:  float = Field(
        ...,
        description=" ",
        example=0
    )
    
    total_charges:  float = Field(
        ...,
        description=" ",
        example=0
    )
    
    cltv:  int = Field(
        ...,
        description=" ",
        example=0
    )
    
    gender:  str = Field(
        ...,
        description=" ",
        example=0
    )
    
    senior_citizen:  str = Field(
        ...,
        description=" ",
        example=0
    )
    
    partner:  str = Field(
        ...,
        description=" ",
        example=0
    )
    
    dependents:  str = Field(
        ...,
        description=" ",
        example=0
    )
    
    phone_service:  str = Field(
        ...,
        description=" ",
        example=0
    )
    
    multiple_lines:  str = Field(
        ...,
        description=" ",
        example=0
    )
    
    internet_service:  str = Field(
        ...,
        description=" ",
        example=0
    )
    
    online_security:  str = Field(
        ...,
        description=" ",
        example=0
    )
    
    online_backup:  str = Field(
        ...,
        description=" ",
        example=0
    )
    
    device_protection:  str = Field(
        ...,
        description=" ",
        example=0
    )
    
    tech_support:  str = Field(
        ...,
        description=" ",
        example=0
    )
    
    streaming_tv:  str = Field(
        ...,
        description=" ",
        example=0
    )
    
    streaming_movies:  str = Field(
        ...,
        description=" ",
        example=0
    )
    
    contract:  str = Field(
        ...,
        description=" ",
        example=0
    )
    
    paperless_billing:  str = Field(
        ...,
        description=" ",
        example=0
    )
    
    payment_method:  str = Field(
        ...,
        description=" ",
        example=0
    )

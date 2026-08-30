from pydantic import BaseModel, Field


class RequestPayload(BaseModel):
    """
    Request body model to predict a unique customer churn probabily.
    
    Attributes:
    """
    
    customer_id: str = Field(
        ...,
        description="ID único que identifica cada cliente.",
        examples=["6176-YJWAS"]
    )
    
    tenure_months: int = Field(
        ...,
        description="Indica a quantidade total de meses que o cliente é um cliente até a data.",
        examples=[3]
    )
    
    monthly_charges:  float = Field(
        ...,
        description="Indica o valor mensal total cobrado do cliente pelos serviços fornecidos pela companhia.",
        examples=[60.0]
    )
    
    total_charges:  float = Field(
        ...,
        description="Indica o valor total cobrado do cliente, calculado até a data.",
        examples=[200.0]
    )
    
    cltv:  int = Field(
        ...,
        description="Customer Lifetime Value. Calculated value.",
        examples=[1500]
    )
    
    gender:  str = Field(
        ...,
        description="O gênero do cliente.",
        examples=["Male", "Female"]
    )
    
    senior_citizen:  str = Field(
        ...,
        description="Indica se o cliente tem mais de 65 anos",
        examples=["Yes", "No"]
    )
    
    partner:  str = Field(
        ...,
        description="Indica se o cliente tem um(a) parceiro(a).",
        examples=["Yes", "No"]
    )
    
    dependents:  str = Field(
        ...,
        description="Indica se o cliente vive com dependentes.",
        examples=["Yes", "No"]
    )
    
    phone_service:  str = Field(
        ...,
        description="Indica se o cliente assina um serviço de linha telefônica fixa com a companhia.",
        examples=["Yes", "No"]
    )
    
    multiple_lines:  str = Field(
        ...,
        description="Indica se o cliente assina múltiplas linhas telefônicas com a companhia.",
        examples=["Yes", "No"]
    )
    
    internet_service:  str = Field(
        ...,
        description="Indica se o cliente assina um serviço de Internet com a companhia.",
        examples=["No", "DSL", "Fiber optic", "Cable"]
    )
    
    online_security:  str = Field(
        ...,
        description="Indica se o cliente assina um serviço adicional de segurança online fornecido pela companhia",
        examples=["Yes", "No"]
    )
    
    online_backup:  str = Field(
        ...,
        description="Indica se o cliente assina um serviço adicional de backup online fornecido pela companhia.",
        examples=["Yes", "No"]
    )
    
    device_protection:  str = Field(
        ...,
        description="Indica se o cliente assina um plano adicional de proteção para dispositivos fornecido pela companhia para o seu equipamento de Internet",
        examples=["Yes", "No"]
    )
    
    tech_support:  str = Field(
        ...,
        description="Indica se o cliente assina um plano adicional de suporte técnico da companhia com tempo de espera reduzido",
        examples=["Yes", "No"]
    )
    
    streaming_tv:  str = Field(
        ...,
        description="Indica se o cliente usa seu serviço de Internet para o stream de programação de televisão de um fornecedor terceiro.",
        examples=["Yes", "No"]
    )
    
    streaming_movies:  str = Field(
        ...,
        description="Indica se o cliente usa seu serviço de Internet para o stream de filmes de um fornecedor terceiro",
        examples=["Yes", "No"]
    )
    
    contract:  str = Field(
        ...,
        description="Indica o tipo de contrato atual do cliente.",
        examples=["Month-to-month", "One year", "Two year"]
    )
    
    paperless_billing:  str = Field(
        ...,
        description="Indica se o cliente escolheu cobrança virtual.",
        examples=["Yes", "No"]
    )
    
    payment_method:  str = Field(
        ...,
        description="Indica como o cliente paga sua conta.",
        examples=[
            "Bank transfer (automatic)",
            "Credit card (automatic)",
            "Mailed check",
        ]
    )

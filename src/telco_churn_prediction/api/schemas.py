"""Request and response contracts for the prediction API."""

from pydantic import BaseModel, Field


class RequestPayload(BaseModel):
    """
    Customer attributes accepted by the prediction endpoint.
    """

    customer_id: str = Field(
        description="Unique customer identifier.")

    tenure_months: int = Field(
        description="Customer tenure in months.")

    monthly_charges: float = Field(
        description="Current monthly charge.")

    total_charges: float = Field(
        description="Accumulated customer charges.")

    cltv: int = Field(
        description="Customer lifetime value.")

    gender: str = Field(
        description="O gênero do cliente.",
        examples=["Male", "Female"])

    senior_citizen: str = Field(
        description="Indica se o cliente tem mais de 65 anos",
        examples=["Yes", "No"])

    partner: str = Field(
        description="Indica se o cliente tem um(a) parceiro(a).",
        examples=["Yes", "No"])

    dependents: str = Field(
        description="Indica se o cliente vive com dependentes.",
        examples=["Yes", "No"])

    phone_service: str = Field(
        description="Indica se o cliente assina um serviço de linha telefônica fixa com a companhia.",
        examples=["Yes", "No"])

    multiple_lines: str = Field(
        description="Indica se o cliente assina múltiplas linhas telefônicas com a companhia.",
        examples=["Yes", "No"])

    internet_service: str = Field(
        description="Indica se o cliente assina um serviço de Internet com a companhia.",
        examples=["No", "DSL", "Fiber optic", "Cable"])

    online_security: str = Field(
        description="Indica se o cliente assina um serviço adicional de segurança online fornecido pela companhia",
        examples=["Yes", "No"])

    online_backup: str = Field(
        description="Indica se o cliente assina um serviço adicional de backup online fornecido pela companhia.",
        examples=["Yes", "No"])

    device_protection: str = Field(
        description="Indica se o cliente assina um plano adicional de proteção para dispositivos fornecido pela companhia para o seu equipamento de Internet",
        examples=["Yes", "No"])

    tech_support: str = Field(
        description="Indica se o cliente assina um plano adicional de suporte técnico da companhia com tempo de espera reduzido",
        examples=["Yes", "No"])

    streaming_tv: str = Field(
        description="Indica se o cliente usa seu serviço de Internet para o stream de programação de televisão de um fornecedor terceiro.",
        examples=["Yes", "No"])

    streaming_movies: str = Field(
        description="Indica se o cliente usa seu serviço de Internet para o stream de filmes de um fornecedor terceiro",
        examples=["Yes", "No"])

    contract: str = Field(
        description="Indica o tipo de contrato atual do cliente.",
        examples=["Month-to-month", "One year", "Two year"])

    paperless_billing: str = Field(
        description="Indica se o cliente escolheu cobrança virtual.",
        examples=["Yes", "No"])

    
    payment_method: str = Field(
        
        description="Indica como o cliente paga sua conta.",
        examples=[
            "Bank transfer (automatic)",
            "Credit card (automatic)",
            "Mailed check",
        ])



class ChurnPrediction(BaseModel):
    """
    Prediction returned by the trained classifier.
    """

    prediction: int
    probability: float | None = None


class PredictResponse(BaseModel):
    """
    Prediction response associated with a customer.
    
    Returns: 
        object: customer_id, churn_predict
    """

    customer_id: str
    churn_predict: ChurnPrediction

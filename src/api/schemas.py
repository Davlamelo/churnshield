from pydantic import BaseModel, Field
from typing import Literal


class CustomerFeatures(BaseModel):
    """Input schema — customer features for churn prediction."""

    SeniorCitizen: int = Field(..., ge=0, le=1,
                               description="1 if senior citizen, 0 otherwise")
    Partner: int = Field(..., ge=0, le=1,
                         description="1 if has partner, 0 otherwise")
    Dependents: int = Field(..., ge=0, le=1,
                            description="1 if has dependents, 0 otherwise")
    tenure: float = Field(..., description="Scaled tenure in months")
    InternetService: Literal["DSL", "Fiber optic", "No"] = Field(
        ..., description="Internet service type")
    Contract: Literal["Month-to-month", "One year", "Two year"] = Field(
        ..., description="Contract type")
    PaperlessBilling: int = Field(..., ge=0, le=1)
    PaymentMethod: Literal[
        "Electronic check", "Mailed check",
        "Bank transfer (automatic)", "Credit card (automatic)"
    ] = Field(..., description="Payment method")
    MonthlyCharges: float = Field(..., gt=0)
    MultipleLines: Literal["Yes", "No", "No phone service"]
    OnlineSecurity: Literal["Yes", "No", "No internet service"]
    OnlineBackup: Literal["Yes", "No", "No internet service"]
    DeviceProtection: Literal["Yes", "No", "No internet service"]
    TechSupport: Literal["Yes", "No", "No internet service"]
    StreamingTV: Literal["Yes", "No", "No internet service"]
    StreamingMovies: Literal["Yes", "No", "No internet service"]
    HasFamily: int = Field(..., ge=0, le=1)
    EngagementScore: int = Field(..., ge=0, le=6)
    ChargePerTenure: float = Field(..., gt=0)


class PredictionResponse(BaseModel):
    """Output schema — churn prediction result."""
    churn_prediction: int
    churn_probability: float
    risk_level: str
    message: str
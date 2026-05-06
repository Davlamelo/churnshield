import pickle
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.api.schemas import CustomerFeatures, PredictionResponse

# --- App initialization ---
app = FastAPI(
    title="ChurnShield API",
    description="Customer churn prediction API powered by XGBoost",
    version="1.0.0"
)

# --- CORS middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# --- Load model and feature names ---
with open("models/best_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("models/feature_names.pkl", "rb") as f:
    feature_names = pickle.load(f)


def preprocess_input(customer: CustomerFeatures) -> pd.DataFrame:
    """Transform raw input into model-ready features."""

    # Encodings matching feature engineering step
    contract_map = {"Month-to-month": 0, "One year": 1, "Two year": 2}
    payment_map = {
        "Electronic check": 0, "Mailed check": 1,
        "Bank transfer (automatic)": 2, "Credit card (automatic)": 3
    }

    base = {
        "SeniorCitizen": customer.SeniorCitizen,
        "Partner": customer.Partner,
        "Dependents": customer.Dependents,
        "tenure": customer.tenure,
        "PaperlessBilling": customer.PaperlessBilling,
        "MonthlyCharges": customer.MonthlyCharges,
        "Contract": contract_map[customer.Contract],
        "PaymentMethod": payment_map[customer.PaymentMethod],
        "HasFamily": customer.HasFamily,
        "EngagementScore": customer.EngagementScore,
        "ChargePerTenure": customer.ChargePerTenure,
    }

    # One-hot encoding for categorical features
    ohe_fields = {
        "InternetService": ["Fiber optic", "No"],
        "MultipleLines": ["No phone service", "Yes"],
        "OnlineSecurity": ["No internet service", "Yes"],
        "OnlineBackup": ["No internet service", "Yes"],
        "DeviceProtection": ["No internet service", "Yes"],
        "TechSupport": ["No internet service", "Yes"],
        "StreamingTV": ["No internet service", "Yes"],
        "StreamingMovies": ["No internet service", "Yes"],
    }

    for col, categories in ohe_fields.items():
        value = getattr(customer, col)
        for cat in categories:
            col_name = f"{col}_{cat}"
            base[col_name] = 1 if value == cat else 0

    df = pd.DataFrame([base])

    # Align columns with training features
    df = df.reindex(columns=feature_names, fill_value=0)

    return df


# --- Routes ---
@app.get("/")
def root():
    return {"message": "ChurnShield API is running 🚀",
            "version": "1.0.0",
            "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/predict", response_model=PredictionResponse)
def predict(customer: CustomerFeatures):
    try:
        df = preprocess_input(customer)
        prediction = int(model.predict(df)[0])
        probability = float(model.predict_proba(df)[0][1])

        if probability >= 0.7:
            risk_level = "HIGH"
            message = "⚠️ High churn risk — immediate retention action recommended"
        elif probability >= 0.4:
            risk_level = "MEDIUM"
            message = "🔔 Medium churn risk — monitor this customer closely"
        else:
            risk_level = "LOW"
            message = "✅ Low churn risk — customer appears stable"

        return PredictionResponse(
            churn_prediction=prediction,
            churn_probability=round(probability, 4),
            risk_level=risk_level,
            message=message
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
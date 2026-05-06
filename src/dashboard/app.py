import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# --- Page config ---
st.set_page_config(
    page_title="ChurnShield",
    page_icon="🛡️",
    layout="wide"
)

# --- Header ---
st.title("🛡️ ChurnShield")
st.markdown("**Customer Churn Prediction Dashboard**")
st.markdown("---")

# --- Sidebar : Customer Input ---
st.sidebar.header("📋 Customer Profile")

# Demographics
st.sidebar.subheader("Demographics")
senior = st.sidebar.selectbox("Senior Citizen", [0, 1],
                               format_func=lambda x: "Yes" if x == 1 else "No")
partner = st.sidebar.selectbox("Partner", [0, 1],
                                format_func=lambda x: "Yes" if x == 1 else "No")
dependents = st.sidebar.selectbox("Dependents", [0, 1],
                                   format_func=lambda x: "Yes" if x == 1 else "No")
has_family = 1 if (partner == 1 or dependents == 1) else 0

# Contract & Billing
st.sidebar.subheader("Contract & Billing")
contract = st.sidebar.selectbox("Contract Type", [
    "Month-to-month", "One year", "Two year"])
payment = st.sidebar.selectbox("Payment Method", [
    "Electronic check", "Mailed check",
    "Bank transfer (automatic)", "Credit card (automatic)"])
paperless = st.sidebar.selectbox("Paperless Billing", [0, 1],
                                  format_func=lambda x: "Yes" if x == 1 else "No")

# Services
st.sidebar.subheader("Services")
internet = st.sidebar.selectbox("Internet Service", [
    "Fiber optic", "DSL", "No"])
multiple_lines = st.sidebar.selectbox("Multiple Lines", [
    "Yes", "No", "No phone service"])
online_security = st.sidebar.selectbox("Online Security", [
    "Yes", "No", "No internet service"])
online_backup = st.sidebar.selectbox("Online Backup", [
    "Yes", "No", "No internet service"])
device_protection = st.sidebar.selectbox("Device Protection", [
    "Yes", "No", "No internet service"])
tech_support = st.sidebar.selectbox("Tech Support", [
    "Yes", "No", "No internet service"])
streaming_tv = st.sidebar.selectbox("Streaming TV", [
    "Yes", "No", "No internet service"])
streaming_movies = st.sidebar.selectbox("Streaming Movies", [
    "Yes", "No", "No internet service"])

# Financials
st.sidebar.subheader("Financials")
tenure = st.sidebar.slider("Tenure (months)", 0, 72, 12)
monthly_charges = st.sidebar.slider("Monthly Charges ($)", 18, 120, 65)

# Computed features
engagement_score = sum([
    online_security == "Yes",
    online_backup == "Yes",
    device_protection == "Yes",
    tech_support == "Yes",
    streaming_tv == "Yes",
    streaming_movies == "Yes"
])
charge_per_tenure = round(monthly_charges / (tenure + 1), 2)

# Scaled values
tenure_mean, tenure_std         = 32.42, 24.54
monthly_mean, monthly_std       = 64.80, 30.09
engagement_mean, engagement_std = 1.83, 1.57
cpt_mean, cpt_std               = 5.71, 8.32

tenure_scaled     = round((tenure - tenure_mean) / tenure_std, 4)
monthly_scaled    = round((monthly_charges - monthly_mean) / monthly_std, 4)
engagement_scaled = round((engagement_score - engagement_mean) / engagement_std, 4)
cpt_scaled        = round((charge_per_tenure - cpt_mean) / cpt_std, 4)

# --- Main ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📊 Customer Summary")
    summary_data = {
        "Contract": contract,
        "Internet Service": internet,
        "Tenure": f"{tenure} months",
        "Monthly Charges": f"${monthly_charges}",
        "Engagement Score": f"{engagement_score}/6",
        "Charge per Tenure": charge_per_tenure,
        "Has Family": "Yes" if has_family else "No",
        "Payment Method": payment
    }
    for key, val in summary_data.items():
        st.markdown(f"**{key}:** {val}")

with col2:
    st.subheader("🔮 Churn Prediction")

    if st.button("🚀 Predict Churn Risk", use_container_width=True):
        payload = {
            "SeniorCitizen": senior,
            "Partner": partner,
            "Dependents": dependents,
            "tenure": tenure_scaled,
            "InternetService": internet,
            "Contract": contract,
            "PaperlessBilling": paperless,
            "PaymentMethod": payment,
            "MonthlyCharges": monthly_scaled,
            "MultipleLines": multiple_lines,
            "OnlineSecurity": online_security,
            "OnlineBackup": online_backup,
            "DeviceProtection": device_protection,
            "TechSupport": tech_support,
            "StreamingTV": streaming_tv,
            "StreamingMovies": streaming_movies,
            "HasFamily": has_family,
            "EngagementScore": engagement_score,      # int brut 0-6
            "ChargePerTenure": charge_per_tenure,     # float brut
        }

        try:
            response = requests.post(
                f"{API_URL}/predict",
                json=payload,
                timeout=5
            )
            result = response.json()

            prob = result['churn_probability']
            risk = result['risk_level']

            if risk == "HIGH":
                st.error(f"🔴 **{risk} RISK** — Churn Probability: {prob:.1%}")
            elif risk == "MEDIUM":
                st.warning(f"🟡 **{risk} RISK** — Churn Probability: {prob:.1%}")
            else:
                st.success(f"🟢 **{risk} RISK** — Churn Probability: {prob:.1%}")

            st.markdown(f"_{result['message']}_")
            st.progress(prob)
            st.caption(f"Churn probability: {prob:.1%}")

        except Exception as e:
            st.error(f"❌ API Error — Make sure FastAPI is running: {e}")
# --- Footer ---
st.markdown("---")
st.caption("ChurnShield v1.0 — Powered by XGBoost & FastAPI")
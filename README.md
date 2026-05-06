# 🛡️ ChurnShield — Customer Churn Prediction

![Python](https://img.shields.io/badge/Python-3.11-blue)
![XGBoost](https://img.shields.io/badge/XGBoost-2.1-orange)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.39-red)
![Docker](https://img.shields.io/badge/Docker-ready-blue)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Spaces-yellow)

> **End-to-end Machine Learning project** — Predicting customer churn for a telecom company using XGBoost, deployed with FastAPI and Streamlit.

🚀 **[Live Demo](https://huggingface.co/spaces/Davlamelo/churnshield)** | 📊 **[Notebooks](notebooks/)** | 🤗 **[HuggingFace Space](https://huggingface.co/spaces/Davlamelo/churnshield)**

---

## 📌 Project Overview

ChurnShield predicts whether a telecom customer is likely to churn (cancel their subscription) based on their profile and usage patterns. It covers the full ML lifecycle — from raw data exploration to a deployed, interactive web application.

**Business Impact:**
- Detects **78.9%** of churners before they leave
- Identifies high-risk customers for targeted retention campaigns
- Key insight: month-to-month contract customers churn at **42.7%** vs **2.8%** for 2-year contracts

---

## 🏗️ Project Architecture

```
Raw Data → EDA → Feature Engineering → Model Training → FastAPI → Streamlit → HuggingFace
```


```
churnshield/
    ├── data/
    │   ├── raw/                    # Original dataset
    │   └── processed/              # Cleaned & engineered features
    ├── notebooks/
    │   ├── 01_eda.ipynb            # Exploratory Data Analysis
    │   ├── 02_feature_engineering.ipynb
    │   └── 03_modeling.ipynb       # Model training & MLflow tracking
    ├── src/
    │   ├── api/                    # FastAPI application
    │   │   ├── main.py
    │   │   └── schemas.py
    │   └── dashboard/              # Streamlit dashboard
    │       └── app.py
    ├── models/                     # Saved model artifacts
    ├── Dockerfile                  # API container
    ├── Dockerfile.streamlit        # Dashboard container
    └── docker-compose.yml          # Multi-container orchestration

---

## 📊 Model Performance

| Model | F1-Score | ROC-AUC |
|---|---|---|
| **XGBoost Tuned** ⭐ | **0.6237** | 0.8332 |
| Logistic Regression | 0.6063 | 0.8372 |
| XGBoost (baseline) | 0.5902 | 0.8107 |
| Random Forest | 0.5309 | 0.8129 |

**Best Model:** XGBoost with GridSearchCV tuning
- `learning_rate=0.01`, `max_depth=7`, `n_estimators=200`, `subsample=0.8`

**Top Features (by importance):**

| Feature | Importance | Business Insight |
|---|---|---|
| Contract | 52% | Monthly contracts = highest churn risk |
| InternetService_Fiber | 14.5% | Fiber optic customers churn 2x more |
| ChargePerTenure | 3.2% | New high-paying customers at risk |

---

## 🔑 Key Findings

- **Contract type** is the strongest churn predictor (52% feature importance)
- Customers with **electronic check** payment churn at 45.3% vs ~16% for automatic payments
- **Senior citizens** churn at 41.7% — nearly 2x the average
- Engineered feature **ChargePerTenure** ranks in Top 5 — validates feature engineering value

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Data Analysis | Pandas, NumPy, Matplotlib, Seaborn |
| Machine Learning | Scikit-learn, XGBoost |
| Experiment Tracking | MLflow |
| API | FastAPI, Pydantic, Uvicorn |
| Dashboard | Streamlit |
| Containerization | Docker, Docker Compose |
| Deployment | HuggingFace Spaces |
| Version Control | Git, GitHub |

---

## 🚀 Quick Start

### Local Setup

```bash
# Clone the repository
git clone https://github.com/Davlamelo/churnshield.git
cd churnshield

# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows
pip install -r requirements.txt

# Run the API
uvicorn src.api.main:app --reload

# Run the dashboard (new terminal)
streamlit run src/dashboard/app.py
```

### Docker

```bash
docker compose up --build
```

---

## 📁 Dataset

**Telco Customer Churn** — IBM Watson Analytics
- 7,043 customers, 21 features
- Target: `Churn` (Yes/No)
- Source: [Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)

---

## 👤 Author

**Ulrich David TASSEMBEDO**
- GitHub: [@Davlamelo](https://github.com/Davlamelo)
- HuggingFace: [@Davlamelo](https://huggingface.co/Davlamelo)

---

## 📄 License

This project is licensed under the MIT License.
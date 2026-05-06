.PHONY: install run-api run-dashboard run-all clean

## Install dependencies
install:
	pip install -r requirements.txt

## Run FastAPI
run-api:
	uvicorn src.api.main:app --reload --port 8000

## Run Streamlit dashboard
run-dashboard:
	streamlit run src/dashboard/app.py

## Run both (API + Dashboard)
run-all:
	uvicorn src.api.main:app --port 8000 & streamlit run src/dashboard/app.py

## Docker build and run
docker-up:
	docker compose up --build

## Clean cache
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
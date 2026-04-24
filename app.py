from fastapi import FastAPI
from pydantic import BaseModel
from src.pipeline.prediction_pipeline import PredictionPipeline

app = FastAPI()

pipeline = PredictionPipeline()

class ChurnRequest(BaseModel):
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float


@app.get("/")
def home():
    return {"message": "Churn Prediction API Running 🚀"}


@app.post("/predict")
def predict(data: ChurnRequest):
    input_data = data.dict()

    prediction = pipeline.predict(input_data)

    result = "Yes" if prediction == 1 else "No"

    return {
        "prediction": result
    }
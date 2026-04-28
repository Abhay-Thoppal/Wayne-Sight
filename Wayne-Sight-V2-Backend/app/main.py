from fastapi import FastAPI
from app.schemas import SequenceInput, PredictionOutput
from app.inference import predict
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Wayne-Sight API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Wayne-Sight Backend Running 👁️"}

@app.post("/predict", response_model=PredictionOutput)
def predict_endpoint(data: SequenceInput):
    prediction, confidence = predict(data.sequence)

    return {
        "prediction": prediction,
        "confidence": confidence
    }
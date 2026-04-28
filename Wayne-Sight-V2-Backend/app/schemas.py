from pydantic import BaseModel
from typing import List

class SequenceInput(BaseModel):
    sequence: List[List[float]]

class PredictionOutput(BaseModel):
    prediction: str
    confidence: float
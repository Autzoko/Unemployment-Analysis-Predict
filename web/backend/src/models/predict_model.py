from pydantic import BaseModel

class UnemploymentRatePrediction(BaseModel):
    state: str
    year: int
    month: int
    unemployment_rate: float

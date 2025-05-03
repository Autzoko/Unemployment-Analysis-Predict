from pydantic import BaseModel

class Prediction(BaseModel):
    state: str
    year: int
    month: int
    unemployment_rate: float

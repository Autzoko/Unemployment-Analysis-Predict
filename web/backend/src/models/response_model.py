from pydantic import BaseModel

class UnemploymentRateResponse(BaseModel):
    state: str
    value: float
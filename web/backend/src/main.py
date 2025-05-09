from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import ValidationError
from typing import List
from services.data_service import get_unemployment_data, get_unemployment_prediction
from models.response_model import UnemploymentRateResponse
from models.predict_model import UnemploymentRatePrediction
from utils.mongo_client import close_mongo_client
#from services.database import prediction_collection
#from web.backend.src.models.predict_model import Prediction

from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    close_mongo_client()

app = FastAPI(title="Unemployment Data API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 或 ["*"] 仅开发时使用
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/unemployment/past", response_model=List[UnemploymentRateResponse])
async def get_unemployment(year: int, month: int):
    try:
        if not 1 <= month <= 12:
            raise HTTPException(status_code=400, detail="Month must between 1 to 12")
        
        data = get_unemployment_data(year, month)

        if not data:
            raise HTTPException(status_code=404, detail="No data found for the specified year and month")
        
        return data
    
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# @app.get("/unemployment/predict", response_model=Prediction)
# async def get_unemployment_rate(state: str, year: int, month: int):
#     query = {"state": state, "year": year, "month": month}
#     prediction = await prediction_collection.find_one(query)
#     if prediction:
#         return Prediction(**prediction)
#     raise HTTPException(status_code=404, detail="Data not found")

@app.get("/unemployment/predict", response_model=UnemploymentRatePrediction)
async def get_prediction(state: str, year: int, month: int):
    try:
        if not 1 <= month <= 12:
            raise HTTPException(status_code=400, detail="Month must between 1 to 12")
        
        data = get_unemployment_prediction(state, year, month)

        if not data:
            raise HTTPException(status_code=404, detail="No prediction data found")
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    

@app.get("/health")
def health():
    return {"status": "ok"}
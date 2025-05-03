from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import ValidationError
from typing import List
from services.data_service import get_unemployment_data
from models.response_model import UnemploymentRateResponse
from utils.mongo_client import close_mongo_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    close_mongo_client()

app = FastAPI(title="Unemployment Data API")

@app.get("/unemployment", response_model=List[UnemploymentRateResponse])
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
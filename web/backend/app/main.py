from fastapi import FastAPI
from app.routers import unemployment, forcast, basic_info

app = FastAPI()

app.include_router(basic_info.router, prefix="/api")
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.database import engine, Base
from models import User   # 👈 MUST IMPORT MODELS
from api.v1.api_router import api_router

app = FastAPI(title="Inventory Management API")

# 👇 CREATE TABLES
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str = "SUPER_SECRET_KEY"
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"
        extra = "ignore"

load_dotenv()

db = os.getenv("DATABASE_URL")

settings = Settings(db)
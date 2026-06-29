from pydantic import ValidationError
from pydantic_settings import BaseSettings # pyright: ignore[reportMissingImports]
class Settings(BaseSettings):
    groq_api:str
    class Config:
        env_file=".env"
try:
    settings=Settings()
except ValidationError as e: 
    print("error")

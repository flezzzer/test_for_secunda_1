from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_KEY: str
    DATABASE_URL: str
    MAX_ACTIVITY_DEPTH: int = 3

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

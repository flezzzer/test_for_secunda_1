from fastapi import Header, HTTPException
from app.core.config import settings
from app.core.db import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def require_api_key(x_api_key: str = Header(...)):
    print("Loaded API_KEY:", settings.API_KEY)
    if x_api_key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="invalid API key")
    return x_api_key

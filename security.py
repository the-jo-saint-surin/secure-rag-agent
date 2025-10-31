
import os
from fastapi import Header, HTTPException, status

APP_API_KEY = os.getenv("APP_API_KEY", "local-dev-key")

def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key is None or x_api_key != APP_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key.",
        )
    return True

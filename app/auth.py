import os
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Header

SECRET = os.getenv("JWT_SECRET", "devsecret")
ALGO = "HS256"

def create_access_token(subject: str, expires_minutes=15):
    payload = {"sub": subject, "exp": datetime.utcnow() + timedelta(minutes=expires_minutes)}
    return jwt.encode(payload, SECRET, algorithm=ALGO)

def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET, algorithms=[ALGO])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing/Invalid token")
    token = authorization.split(" ", 1)[1]
    payload = decode_token(token)
    return payload["sub"]

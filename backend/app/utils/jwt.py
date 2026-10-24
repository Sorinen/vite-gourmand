from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
import os

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def get_secret_key() -> str:
    key = os.getenv("SECRET_KEY", "").strip()
    if not key:
        raise RuntimeError("SECRET_KEY est absente ou vide : definissez-la dans l'environnement")
    return key

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, get_secret_key(), algorithm=ALGORITHM)

def verify_token(token: str) -> dict:
    key = get_secret_key()
    try:
        payload = jwt.decode(token, key, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

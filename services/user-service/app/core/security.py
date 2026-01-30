from datetime import datetime, timedelta
from typing import Optional
import bcrypt
from jose import JWTError, jwt
from app.core.config import settings

# bcrypt has a 72-byte limit; passlib's internal check can fail in some environments, so we use bcrypt directly.
BCRYPT_MAX_PASSWORD_BYTES = 72


def _to_bytes(password: str) -> bytes:
    pwd_bytes = password.encode("utf-8")
    if len(pwd_bytes) > BCRYPT_MAX_PASSWORD_BYTES:
        pwd_bytes = pwd_bytes[:BCRYPT_MAX_PASSWORD_BYTES]
    return pwd_bytes


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(_to_bytes(plain_password), hashed_password.encode("utf-8"))


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(_to_bytes(password), bcrypt.gensalt()).decode("utf-8")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError:
        return None


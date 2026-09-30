from datetime import datetime, timedelta, timezone
import jwt
from pwdlib import PasswordHash
from src.core.config import settings

password_hasher = PasswordHash.recommended()
dummy_hash = password_hasher.hash("dummy_password")

def hash_password(password: str) -> str:
    return password_hasher.hash(password)

def verify_password(raw_password: str, hashed_password: str) -> bool:
    return password_hasher.verify(raw_password, hashed_password)

def create_token(subject: str, token_type: str, expires_delta: timedelta) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": subject,
        "type": token_type,
        "iat": now,
        "exp": now + expires_delta
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.algorithm)

def decode_token (token: str, expected_type: str) -> dict:
    payload = jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.algorithm],
        options={"require": ["exp", "sub"]}
    )
    if payload.get("type") != expected_type:
        raise jwt.InvalidTokenError("Invalid token type")
    return payload
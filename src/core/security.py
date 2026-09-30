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


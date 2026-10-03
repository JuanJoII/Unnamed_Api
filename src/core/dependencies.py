from typing import Annotated
import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from uuid import UUID

from src.db.db_conn import SessionLocal
from src.core.security import decode_token
from src.db.db_models import User
from src.core.exceptions import UNAUTHORIZED

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DBSession = Annotated[Session, Depends(get_db)]


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: DBSession
) -> User:
    try:
        payload = decode_token(token, expected_type="access")
    except jwt.InvalidTokenError:
        raise UNAUTHORIZED

    user_id = UUID(payload.get("sub"))
    user = db.get(User, user_id)
    if user is None:
        raise UNAUTHORIZED
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]

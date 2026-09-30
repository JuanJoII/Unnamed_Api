from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
import jwt
import uuid
from sqlalchemy import select

from src.db.db_models import User
from src.schemas.tokens import Token
from src.services.token_service import issue_tokens
from src.core.dependencies import DBSession
from src.core.security import decode_token, verify_password, dummy_hash
from src.schemas.tokens import RefreshTokenRequest

class AuthService:
    def __init__(self, db: DBSession):
        self.db = db

    def get_token(self, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token | None:
        user = self.db.scalar(select(User).where(User.email == form_data.username))
        hash = (
            user.password_hash if user else dummy_hash
        )  # Use a dummy hash to prevent timing attacks
        password_valid = verify_password(form_data.password, hash)
        if not user or not password_valid:
            return None

        credentials = issue_tokens(user.id)
        user.refresh_token = credentials.refresh_token
        self.db.commit()

        return credentials

    def get_refresh_token(self, body: RefreshTokenRequest) -> Token | None:
        try:
            payload = decode_token(body.refresh_token, expected_type="refresh")
        except jwt.InvalidTokenError:
            return None
        user = self.db.get(User, uuid.UUID(payload.get("sub")))
        if not user:
            return None
        return issue_tokens(user.id)
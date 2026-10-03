from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.db.db_models import User
from src.schemas.tokens import TokenResponse
from src.schemas.user import UserCreate
from src.core.dependencies import DBSession
from src.core.security import hash_password, verify_password, dummy_hash
from src.core.config import settings
from src.services.token_service import TokenService


def get_token_service(db: DBSession, settings: settings) -> TokenService:
    return TokenService(db=db, settings=settings)


TokenServiceDep = Annotated[TokenService, Depends(get_token_service)]


class AuthService:
    def __init__(self, db: DBSession, tokens: TokenServiceDep):
        self._db = db
        self._tokens = tokens

    def _issue_tokens(self, user: User) -> TokenResponse:
        access_token = self._tokens.generate_access_token(user=user)
        refresh_token = self._tokens.generate_and_save_refresh_token(user=user)
        return TokenResponse(
            user_id=user.id, access_token=access_token, refresh_token=refresh_token
        )

    def login(
        self, form: Annotated[OAuth2PasswordRequestForm, Depends()]
    ) -> TokenResponse | None:
        user = self._db.scalar(select(User).where(User.email == form.username))

        hashed_password = user.password_hash if user else dummy_hash
        password_valid = verify_password(form.password, hashed_password)

        if user is None or not password_valid:
            return None

        return self._issue_tokens(user)

    def create_user(self, api_user: UserCreate) -> User | None:
        hashed_password = hash_password(api_user.password)
        db_user = User(
            email=api_user.email,
            password_hash=hashed_password,
            username=api_user.username,
        )
        self._db.add(db_user)
        try:
            self._db.commit()
        except IntegrityError:
            self._db.rollback()
            return None
        self._db.refresh(db_user)
        return db_user

    def logout(self, user: User):
        self._tokens.revoke_refresh_token(user)

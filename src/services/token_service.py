import uuid
import secrets
from datetime import timedelta, timezone, datetime
from src.core.security import create_token
from src.core.config import settings
from src.core.dependencies import DBSession
from src.db.db_models import User
from src.core.security import create_token, hash_password, verify_password
from src.schemas.tokens import TokenResponse, RefreshTokenRequest


class TokenService:
    def __init__(self, db: DBSession, settings: settings):
        self._db = db
        self._settings = settings

    def generate_access_token(self, user: User):
        now = datetime.now(timezone.utc)
        payload = {
            "sub": str(user.id),
            "email": user.email,
            "iat": now,
            "exp": now + timedelta(minutes=self._settings.access_token_expire_minutes),
            "type": "access",
        }
        token = create_token(payload)
        return token

    def generate_and_save_refresh_token(self, user: User):
        refresh_token = secrets.token_urlsafe(32)
        user.refresh_token_hash = hash_password(refresh_token)
        user.refresh_token_expire_date = datetime.now(timezone.utc) + timedelta(days=self._settings.refresh_token_expire_days)
        self._db.commit()
        return refresh_token

    def validate_refresh_token(self, user_id: uuid.UUID, refresh_token: str) -> User | None:
        user = self._db.get(User, user_id)
        if user is None or user.refresh_token_hash is None or user.refresh_token_expire_date is None:
            return None
        if user.refresh_token_expire_date is None or user.refresh_token_expire_date <= datetime.now(timezone.utc):
            return None
        if verify_password(refresh_token, user.refresh_token_hash) is False:
            return None
        return user

    def renew_tokens(self, refresh_request: RefreshTokenRequest) -> TokenResponse | None:
        user = self.validate_refresh_token(refresh_request.user_id, refresh_request.refresh_token)
        if user is None:
            return None
        new_access_token = self.generate_access_token(user)
        new_refresh_token = self.generate_and_save_refresh_token(user)
        return TokenResponse(user_id=user.id, access_token=new_access_token, refresh_token=new_refresh_token)

    def revoke_refresh_token(self, user: User):
        user.refresh_token_hash = None
        user.refresh_token_expire_date = None
        self._db.commit()
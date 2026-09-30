import uuid
from datetime import timedelta
from src.core.security import create_token
from src.schemas.tokens import Token
from src.core.config import settings


def issue_tokens(user_id: uuid.UUID) -> Token:
    access_token = create_token(
        str(user_id),
        token_type="access",
        expire_delta=timedelta(minutes=settings.access_token_expire_minutes),
    )
    refresh_token = create_token(
        str(user_id),
        token_type="refresh",
        expire_delta=timedelta(days=settings.refresh_token_expire_days),
    )
    return Token(access_token=access_token, refresh_token=refresh_token)

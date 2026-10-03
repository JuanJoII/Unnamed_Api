from pydantic import BaseModel
from uuid import UUID


class TokenResponse(BaseModel):
    user_id: UUID
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    user_id: UUID
    refresh_token: str

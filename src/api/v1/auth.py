from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from src.services.auth_service import AuthService
from src.schemas.tokens import Token, RefreshTokenRequest
from src.core.dependencies import DBSession


router = APIRouter(prefix="/auth", tags=["Authentication"])

def get_auth_service(db_session: DBSession) -> AuthService:
    return AuthService(db=db_session)


@router.post("/get_token", model_response=Token)
def get_token_endpoint(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: AuthService = Depends(get_auth_service),
) -> Token:
    token = auth_service.get_token(form_data)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales invalidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token


@router.post("/get_refresh", model_response=Token)
def get_refresh_token_endpoint(body: RefreshTokenRequest, auth_service: AuthService = Depends(get_auth_service)) -> Token:
    token = auth_service.get_refresh_token(body=body)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales Invalidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token
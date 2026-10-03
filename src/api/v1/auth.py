from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from src.schemas.tokens import TokenResponse, RefreshTokenRequest
from src.schemas.user import UserCreate
from src.core.exceptions import UNAUTHORIZED, USERALREADYEXISTS
from src.core.dependencies import CurrentUser
from src.services.token_service import TokenService
from src.services.auth_service import AuthService
from src.core.dependencies import DBSession
from src.core.config import settings


router = APIRouter(prefix="/auth", tags=["Authentication"])

def get_token_service(db: DBSession) -> TokenService:
    return TokenService(db=db, settings=settings)

TokenServiceDep = Annotated[TokenService, Depends(get_token_service)]

def get_auth_service(db_session: DBSession, token_service: TokenServiceDep) -> AuthService:
    return AuthService(db=db_session, tokens=token_service)

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]

@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login_endpoint( form_data : Annotated[OAuth2PasswordRequestForm, Depends()], auth_service: AuthServiceDep) -> TokenResponse:
    login_response = auth_service.login(form=form_data)
    if login_response is None:
        raise UNAUTHORIZED

    return login_response

@router.post("/refresh", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def renew_tokens_endpoint(refresh: RefreshTokenRequest, token_service: TokenServiceDep) -> TokenResponse:
    new_token = token_service.renew_tokens(refresh)
    if new_token is None:
        raise UNAUTHORIZED
    return new_token

@router.post("/logout", status_code=status.HTTP_200_OK)
def logout_endpoint(user: CurrentUser, auth_service: AuthServiceDep):
    try:
        auth_service.logout(user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return {"message": "Successfully logged out."}

@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
def register_user_endpoint(user: UserCreate, auth_service: AuthServiceDep) -> dict:
    register_response = auth_service.create_user(user)
    if register_response is None:
        raise USERALREADYEXISTS
    return {"message": "User registered successfully.", "user": register_response.username}


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.db_conn import get_db
from src.services.user_service import UserServices
from src.models.user import UserCreate, UserRead, UserLogin
import uuid

router = APIRouter(prefix="/users", tags=["users"])

def get_user_service(db: Session = Depends(get_db)) -> UserServices:
    return UserServices(db)

@router.post("/", response_model=UserRead, status_code=201)
def create_user_endpoint(user: UserCreate, user_service: UserServices = Depends(get_user_service)) -> UserRead:
    db_user = user_service.create_user(user)
    if not db_user:
        raise HTTPException(status_code=400, detail="User could not be created")
    return db_user

@router.get("/all", response_model=list[UserRead])
def get_all_users_endpoint(user_service: UserServices = Depends(get_user_service)) -> list[UserRead]:
    return user_service.get_all_users()

@router.post("/login", response_model=dict, status_code=200)
def login_user_endpoint(login_data: UserLogin, user_service: UserServices = Depends(get_user_service)) -> dict:
    result = user_service.login_user(login_data.email, login_data.password)
    if result:
        return {"message": result}

    raise HTTPException(status_code=401, detail="Invalid email or password")

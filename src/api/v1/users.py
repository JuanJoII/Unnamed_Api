from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.db_conn import get_db
from src.services.user_service import create_user, get_all_users
from src.models.user import UserCreate, UserRead
import uuid

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserRead, status_code=201)
async def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)) -> UserRead:
    db_user = await create_user(db, user)
    if not db_user:
        raise HTTPException(status_code=400, detail="User could not be created")
    return db_user

@router.get("/all", response_model=list[UserRead])
async def get_all_users_endpoint(db: Session = Depends(get_db)):
    return await get_all_users(db)

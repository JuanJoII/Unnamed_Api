from sqlalchemy.orm import Session
from src.db.schemas import User
from src.models.user import UserCreate, UserRead
import uuid

async def create_user(db: Session, api_user: UserCreate) -> User:
    db_user = User(
        email=api_user.email,
        password=api_user.password,
        username=api_user.username
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

async def get_all_users(db: Session) -> list[UserRead]:
    users = db.query(User).all()
    return [UserRead.model_validate(user) for user in users]
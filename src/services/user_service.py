from sqlalchemy.orm import Session
from db.db_models import User
from src.schemas.user import UserCreate, UserRead
from src.core.config import phasher
import uuid


class UserServices:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, api_user: UserCreate) -> User:
        hashed_password = phasher.hash(api_user.password)
        db_user = User(
            email=api_user.email, password=hashed_password, username=api_user.username
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_all_users(self) -> list[UserRead]:
        users = self.db.query(User).all()
        return [UserRead.model_validate(user) for user in users]

    def get_user_by_id(self, user_id: uuid.UUID) -> UserRead | None:
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            return UserRead.model_validate(user)
        return None

    def login_user(self, email: str, password: str) -> str | None:
        db_user = self.db.query(User).filter(User.email == email).first()

        if db_user and phasher.verify(db_user.password, password):
            return "Login successful"

        return None

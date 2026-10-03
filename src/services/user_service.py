from src.db.db_models import User
from src.core.dependencies import DBSession
from src.schemas.user import UserRead
import uuid


class UserServices:
    def __init__(self, db: DBSession):
        self.db = db

    def get_all_users(self) -> list[UserRead]:
        users = self.db.query(User).all()
        return [UserRead.model_validate(user) for user in users]

    def get_user_by_id(self, user_id: uuid.UUID) -> UserRead | None:
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            return UserRead.model_validate(user)
        return None

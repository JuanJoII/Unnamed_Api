from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.user_model import User
from src.db.models.mixins import Base

class Profile(Base):
    
    __tablename__ = "profiles"

    user_id: Mapped["User"] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    username: Mapped[str] = mapped_column(String(50),unique=True)
    artist_name: Mapped[str | None] = mapped_column(String(100))
    avatar_key: Mapped[str | None] = mapped_column(String(512))

    user: Mapped["User"] = relationship(back_populates="profile")
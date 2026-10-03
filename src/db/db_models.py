import uuid
import datetime
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from src.db.db_conn import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    username: Mapped[str] = mapped_column(String(255), nullable=False)
    refresh_token_hash: Mapped[str | None] = mapped_column(String(255))
    refresh_token_expire_date: Mapped[datetime.datetime | None] = mapped_column(
        DateTime(timezone=True)
    )

from datetime import datetime
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.models.mixins import Base, UUIDPKMixin, CreatedAtMixin
from src.db.models.refresh_tokens_model import RefreshToken
from src.db.models.profile_model import Profile

class User(Base, UUIDPKMixin, CreatedAtMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    verification_sent_at: Mapped[datetime] = mapped_column(server_default=func.now())
    verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True)) # si null sin verificar

    profile: Mapped["Profile"] = relationship( back_populates="user", cascade="all, delete-orphan", pasive_deletes=True)
    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(back_populates="user", cascade="all, delete-orphan", passive_deletes=True)
from typing import Any
import uuid

from sqlalchemy import ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

from db.models.profile_model import Profile
from src.db.models.mixins import Base, UUIDPKMixin, CreatedAtMixin

class Album(Base, UUIDPKMixin, CreatedAtMixin):
    __tablename__ = "albums"

    uploaded_by_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("profiles.user_id", ondelete="CASCADE"), index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    cover_key: Mapped[str | None] = mapped_column(String(512))
    meta: Mapped[dict[str, Any]] = mapped_column("meta", JSONB, default=dict, nullable=False, server_default=text("'{}'::jsonb"))
    
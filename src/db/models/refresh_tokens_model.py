import uuid
from datetime import datetime
from sqlalchemy import CheckConstraint, Enum, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.types import ClientType
from src.db.models.mixins import Base, UUIDPKMixin, CreatedAtMixin
from src.db.models.user_model import User

class RefreshToken(Base, UUIDPKMixin, CreatedAtMixin):
    __tablename__ = "refresh_tokens"
    __table_args__ = (
        UniqueConstraint("user_id", "client_type", name="uq_user_client_type"),
        CheckConstraint("client_type IN ('app', 'web')", name="client_type_validation"),
    )
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token_hash: Mapped[str] = mapped_column(String(255), unique=True)
    expires_at: Mapped[datetime]
    client_type: Mapped[ClientType] = mapped_column(
        Enum(
            ClientType,
            native_enum=False,
            create_constraint=False,
            length=10,
            values_callable=lambda e: [m.value for m in e],
        )
    )

    user: Mapped["User"] = relationship(back_populates="refresh_tokens")
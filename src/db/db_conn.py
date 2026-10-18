from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from src.core.config import settings

db_url = f"postgresql://{settings.postgres_user.get_secret_value()}:{settings.postgres_password.get_secret_value()}@localhost:5432/{settings.postgres_db}"

engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



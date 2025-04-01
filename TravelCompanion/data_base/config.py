from contextlib import contextmanager

from fastapi import Depends
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, declared_attr, mapped_column, sessionmaker


def get_db():
    db = db_helper.session()
    try:
        yield db
    finally:
        db.close()

class Settings(BaseSettings):
    db_url: str = 'sqlite:///./db.sqlite3'
    db_echo: bool = True

settings = Settings()

class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_engine(url=url, echo = echo, connect_args={"check_same_thread": False})
        self.session = sessionmaker(
            bind = self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

db_helper = DatabaseHelper(url=settings.db_url, echo=settings.db_echo)

class CreateTableHelper(DeclarativeBase):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls) -> str:
        return f'{cls.__name__.lower()}s'

    id: Mapped[int] = mapped_column(primary_key=True)

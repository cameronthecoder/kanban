from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import Session
from sqlmodel import SQLModel
from src.routes import boards
from typing import AsyncGenerator
from sqlalchemy.ext.declarative import declarative_base


engine = create_async_engine(
    "sqlite+aiosqlite:///test.sqlite3",
    connect_args={"check_same_thread": False},
    echo=False,
)
SessionLocal = async_sessionmaker(engine)
Base = declarative_base()


async def get_db() -> AsyncGenerator[Session, None]:
    async with engine.begin() as conn:
        from .models.user import User
        from .models.board import Board, Column, Task

        await conn.run_sync(SQLModel.metadata.create_all)

    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()

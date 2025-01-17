from fastapi import FastAPI
from src.routes import boards
from sqlmodel import SQLModel
from .database import Base, engine, get_db
from contextlib import asynccontextmanager

from .models.user import User
from .models.board import Board, Column, Task

# setup cors
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield


app = FastAPI(title="Kanban", lifespan=lifespan, root_path="/api", debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from src.routes import boards
from src.routes import auth

app.include_router(boards.router)
app.include_router(auth.router)

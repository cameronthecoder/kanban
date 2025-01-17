from fastapi import (
    APIRouter,
    Depends,
    WebSocket,
    WebSocketDisconnect,
    Path,
    HTTPException,
)
from uuid import uuid4, UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import joinedload, selectinload
from pydantic import BaseModel
from typing import List, Annotated
import logging, time
from sqlalchemy import or_

logger = logging.getLogger("uvicorn.info")

router = APIRouter(
    prefix="/boards", tags=["Boards"], responses={404: {"description": "Not found"}}
)
from src.database import get_db
from src.models.user import User
from src.models.board import Board, Column, Task
from .auth import get_current_user

# Buffer for storing incoming updates
pending_updates = []
UPDATE_THRESHOLD = 5  # Send updates after 5 changes
LAST_UPDATE_TIME = time.time()


class BoardCreate(BaseModel):
    name: str


@router.get("/", response_model=List[Board])
async def get_boards(
    db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
):
    results = await db.execute(
        select(Board).where(or_(Board.owner_id == user.id, Board.users.any(id=user.id)))
    )
    logging.debug(results)
    boards = results.scalars().all()
    return boards

@router.get("/add-user/{board_id}/{user_id}/", response_model=Board)
async def add_user_to_board(board_id: Annotated[int, Path(title="The ID of the board to get")], user_id: Annotated[int, Path(title="The ID of the user to get")], db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user),):
    board = await db.get(Board, board_id)
    user = await db.get(User, user_id)
    board.users.append(user)
    await db.commit()
    return board


class ColumnCreate(BaseModel):
    name: str


@router.post("/{board_id}/columns/")
async def add_column_to_board(
    board_id: Annotated[int, Path(title="The ID of the board to get")],
    column: ColumnCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    board = await db.get(Board, board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    if board.owner_id != user.id and user.id not in [u.id for u in board.users]:
        raise HTTPException(
            status_code=403, detail="You do not have access to this board"
        )
    c = Column(**column.model_dump(), board_id=board_id)
    c.board_id = board_id
    db.add(c)
    await db.commit()
    await db.refresh(c)
    return {"column": c.model_dump()}


# get all columns for a board
@router.get("/{board_id}/columns/")
async def get_columns_for_board(
    board_id: Annotated[int, Path(title="The ID of the board to get")],
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    # check if the user has access to the board
    board = await db.get(Board, board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    if board.owner_id != user.id and user.id not in [u.id for u in board.users]:
        raise HTTPException(
            status_code=403, detail="You do not have access to this board"
        )
    result = await db.execute(select(Column).where(Column.board_id == board_id))
    columns = result.scalars().all()
    return columns


# get an individual board and include columns, make sure the columns are included
@router.get("/{board_id}", response_model=Board)
async def get_board(
    board_id: Annotated[int, Path(title="The ID of the board to get")],
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Board)
        .options(joinedload(Board.columns))  # Load related columns
        .where(Board.id == board_id)
    )
    board = result.scalars().first()
    if not board:
        return {"message": "Board not found"}
    if board.owner_id != user.id and user.id not in [u.id for u in board.users]:
        return {"message": "You do not have access to this board"}
    return board


@router.post("/", response_model=Board)
async def create_board(
    board: BoardCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    board = Board(**board.model_dump())
    board.owner_id = user.id
    db.add(board)
    await db.commit()
    return board


import time


class CreateTask(BaseModel):
    name: str
    description: str
    is_dune: bool = False


# add a route to add a task to a column
@router.post("/{board_id}/columns/{column_id}/tasks/")
async def add_task_to_column(
    board_id: Annotated[int, Path(title="The ID of the board to get")],
    column_id: Annotated[int, Path(title="The ID of the column to get")],
    task: CreateTask,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    board = await db.get(Board, board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    if board.owner_id != user.id and user.id not in [u.id for u in board.users]:
        raise HTTPException(
            status_code=403, detail="You do not have access to this board"
        )
    # check if the column belongs to the board
    column = await db.get(Column, column_id)
    if not column:
        raise HTTPException(status_code=404, detail="Column not found")
    if column.board_id != board_id:
        raise HTTPException(
            status_code=403, detail="Column does not belong to this board"
        )
    t = Task(**task.model_dump(), column_id=column_id)
    db.add(t)
    await db.commit()
    await db.refresh(t)
    return {"task": t.model_dump()}

class Connection(BaseModel):
    ws: WebSocket
    id: UUID
    user: User

active_connections: List[Connection] = []

async def broadcast_message(message):
    for connection in active_connections:
        await connection.send_json(message)

# Handle WebSocket messages and batch updates
@router.websocket("/{board_id}/ws/")
async def websocket_endpoint(
    websocket: WebSocket,
    board_id: Annotated[int, Path(title="The ID of the board to get")],
    token: str,
    db: AsyncSession = Depends(get_db),
):
    global pending_updates, LAST_UPDATE_TIME
    uuid = uuid4()
    user = await get_current_user(token, db)
    await websocket.accept()
    await broadcast_message({"type": "connection", "data": {"user": user, "id": str(uuid)}})
    conn = active_connections.append(Connection(ws=websocket, id=uuid, user=user))

    try:

        while True:
            data = await websocket.receive_json()

            match data["type"]:
                case "columns":
                    results = await db.scalars(
                        select(Column)
                        .filter(Column.board_id == board_id)
                        .options(
                            selectinload(
                                Column.tasks.and_(Task.parent_task_id == None)
                            ),
                            joinedload(Column.board),
                        )
                    )
                    columns = results.unique().all()
                    logger.info(("Columns: ", columns))
                    # create an annonmous function that calls the toRead method on each column
                    columns = [c.toRead(c) for c in columns]
                    await websocket.send_json(
                        {"type": "columns", "data": jsonable_encoder(columns)}
                    )
                case "edit_board":
                    print(data)
                    board = await db.get(Board, board_id)
                    if not board:
                        await websocket.send_json(
                            {"type": "error", "message": "Board not found"}
                        )
                        continue
                    board.name = data["data"]["name"]
                    await db.commit()
                    await db.refresh(board)
                    await broadcast_message(
                        {"type": "edit_board", "data": jsonable_encoder(board)}
                    )
                case "add_task":
                    task = Task(**data["data"])
                    db.add(task)
                    print("ADD TASK")
                    print(data)
                    await db.commit()
                    await db.refresh(task)
                    await broadcast_message(
                        {"type": "add_task", "data": jsonable_encoder(task)}
                    )
                case "move_task":
                    task = await db.get(Task, data["data"]["task_id"])
                    task.column_id = data["data"]["to"]
                    await db.commit()
                    await db.refresh(task)
                    await broadcast_message(
                        {"type": "move_task", "data": jsonable_encoder({"task": task, "to": data["data"]["to"]})}
                    )
                case "add_column":
                    column = Column(**data["data"], board_id=board_id)
                    db.add(column)
                    await db.commit()
                    await db.refresh(column)
                    await broadcast_message(
                        {"type": "add_column", "data": jsonable_encoder(column)}
                    )
                case "delete_column":
                    column = await db.get(Column, data["data"]["column_id"])
                    await db.delete(column)
                    await db.commit()
                    await broadcast_message(
                        {"type": "delete_column", "data": jsonable_encoder(column)}
                    )
                case _:
                    print(data)

    except WebSocketDisconnect:
        active_connections.remove(conn)
        await broadcast_message({"type": "disconnection", "data": {"user": user, "id": str(uuid)}})
        print(conn.user.first_name, "disconnected")


async def save_batch_updates(updates):
    # Save updates to database here (this can be optimized)
    pass


@router.delete("/{board_id}")
async def delete_board(
    board_id: Annotated[int, Path(title="The ID of the board to get")],
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    board = await db.get(Board, board_id)
    if not board:
        return {"message": "Board not found"}
    if board.owner_id != user.id:
        return {"message": "You are not the owner of this board"}
    await db.delete(board)
    await db.commit()
    return {"message": "Board deleted"}

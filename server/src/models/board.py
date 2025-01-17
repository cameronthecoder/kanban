from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.orm import relationship
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column


class BoardUsersLink(SQLModel, table=True):
    board_id: Optional[int] = Field(
        default=None, foreign_key="board.id", primary_key=True
    )
    user_id: Optional[int] = Field(
        default=None, foreign_key="user.id", primary_key=True
    )


class Board(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    owner_id: int = Field(default=None, foreign_key="user.id")
    users: list["User"] = Relationship(
        back_populates="boards", link_model=BoardUsersLink
    )
    columns: list["Column"] = Relationship(back_populates="board")



class Column(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    board_id: Optional[int] = Field(default=None, foreign_key="board.id")
    board: Optional[Board] = Relationship(back_populates="columns")
    tasks: list["Task"] = Relationship(back_populates="column")

    @staticmethod
    def toRead(column: "Column") -> "ColumnRead":
        return ColumnRead(
            name=column.name,
            id=column.id,
            board_id=column.board_id,
            board=column.board,
            tasks=column.tasks,
        )

class ColumnRead(BaseModel):
    name: str
    id: int
    board_id: int
    board: Board
    tasks: list["Task"]


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    parent_task_id: Optional[int] = Field(default=None, foreign_key="task.id")
    parent_task: Optional["Task"] = Relationship(back_populates="child_tasks", sa_relationship_kwargs={"remote_side": "Task.id"})
    child_tasks: list["Task"] = Relationship(back_populates="parent_task")
    name: str
    description: str
    is_done: bool = False
    column_id: Optional[int] = Field(default=None, foreign_key="column.id")
    column: Optional[Column] = Relationship(back_populates="tasks")


from .user import User

Board.model_rebuild()

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from typing_extensions import Annotated


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    is_admin: bool = False
    username: str
    password: Annotated[str, Field(exclude=True)]
    boards: List["Board"] = Relationship(back_populates="users")


from .board import Board

User.model_rebuild()

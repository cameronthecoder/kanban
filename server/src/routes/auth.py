from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, field_serializer
from sqlalchemy.ext.asyncio import AsyncSession
from jwt.exceptions import InvalidTokenError
from sqlalchemy.sql import select
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated, Optional
import bcrypt, jwt, json

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)
from src.database import get_db
from src.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token/")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
        data = payload.get("user")
        if payload is None:
            raise credentials_exception
        user = User(**json.loads(data))
    except InvalidTokenError:
        raise credentials_exception
    print(user)
    result = (
        await db.execute(select(User).where(User.username == user.username))
    ).scalar_one_or_none()

    print(result)

    if result is None:
        print("no user")
        raise credentials_exception
    return result


class UserRegister(BaseModel):
    username: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_admin: Optional[bool] = False

    @field_serializer("password")
    def serialize_dt(self, pw: str, _info):
        return bcrypt.hashpw(pw.encode("utf-8"), bcrypt.gensalt())


@router.post(
    "/token", responses={401: {"description": "Incorrect username or password"}}
)
async def token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_db),
):
    result = (
        await db.execute(select(User).where(User.username == form_data.username))
    ).scalar_one_or_none()
    if not result or not bcrypt.checkpw(form_data.password.encode(), result.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    user: User = result

    encoded_jwt = jwt.encode(
        {"user": user.model_dump_json()}, "secret", algorithm="HS256"
    )

    return {"access_token": encoded_jwt, "token_type": "bearer"}


@router.get("/user")
async def get_user(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/register")
async def register(
    user: UserRegister,
    db: AsyncSession = Depends(get_db),
):
    new_user = User(**user.model_dump())
    db.add(new_user)
    await db.commit()
    return new_user


@router.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    results = await db.execute(select(User))
    users = results.scalars().all()
    return users

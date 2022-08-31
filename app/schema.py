from datetime import datetime
import email
from typing import Optional, Type
from fastapi import Form, HTTPException
from pydantic import BaseModel, EmailStr, ValidationError, validator
from pydantic.types import conint
import inspect
from .database import Base


def as_form(cls: Type[BaseModel]):
    """
    Adds an as_form class method to decorated models. The as_form class method
    can be used with FastAPI endpoints
    """
    new_params = [
        inspect.Parameter(
            field.alias,
            inspect.Parameter.POSITIONAL_ONLY,
            default=(Form(field.default) if not field.required else Form(...)),
        )
        for field in cls.__fields__.values()
    ]

    async def _as_form(**data):
        return cls(**data)

    sig = inspect.signature(_as_form)
    sig = sig.replace(parameters=new_params)
    _as_form.__signature__ = sig
    setattr(cls, "as_form", _as_form)
    return cls


@as_form
class UserOut(BaseModel):
    id: int
    fullname: str
    email: EmailStr
    phone_number: int
    created_at: datetime
    image_url: str

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class CreatePost(PostBase):
    pass


class UpdatePost(PostBase):
    pass


class Post(PostBase):
    # pass
    id: int
    title: str
    content: str
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    votes: int


@as_form
class UserCreate(BaseModel):
    fullname: str
    email: EmailStr
    phone_number: str
    password: str

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(UserOut):
    pass
    token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class vote(BaseModel):
    post_id: int
    dir: conint(le=1)


class profile(BaseModel):
    id: int
    image_name: str
    image_url: str

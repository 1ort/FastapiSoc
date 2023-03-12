from pydantic import BaseModel, Field
from typing import Optional


class Message(BaseModel):
    message: str


class PostBase(BaseModel):
    content: str = Field(..., max_length=1500)


class ReactionsCount(BaseModel):
    likes: int = 0
    dislikes: int = 0


class NewPost(PostBase):
    pass


class Post(PostBase):
    id: int
    author_id: int
    reactions_count: ReactionsCount

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserCredentials(UserBase):
    password: str


class User(UserBase):
    id: int
    posts: list[Post] = []

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class PaginationParams(BaseModel):
    skip: Optional[int] = Field(default=0, ge=0)
    limit: Optional[int] = Field(default=50, gt=0, le=100)


class HTTPError(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {"detail": "Error details"},
        }


class Success(BaseModel):
    result: str

from fastapi import FastAPI
from .database import engine
from . import models, schemas

from .routes import account, users, posts

models.Base.metadata.create_all(bind=engine)

tags_metadata = [
    {
        "name": "account",
        "description": "Manage your account",
    },
    {
        "name": "users",
        "description": "View Users",
    },
    {
        "name": "posts",
        "description": "View and manage posts",
    },
    {
        "name": "reactions",
        "description": "Like and dislike other people's posts"
    },
]

app = FastAPI(
    openapi_tags=tags_metadata,
    responses={
        500: {
            "model": schemas.HTTPError,
            "description": "Internal",
        },
    },
)

app.include_router(account.signup_router)
app.include_router(account.router, prefix="/account")
app.include_router(users.router, prefix="/users")
app.include_router(posts.router, prefix="/posts")
app.include_router(posts.manage_post_router, prefix="/posts")

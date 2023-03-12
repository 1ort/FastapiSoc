from sqlalchemy.orm import Session
from .database import SessionLocal
from . import crud, schemas
from fastapi import HTTPException, status, Depends

from .security import oauth2_scheme, verify_jwt_token, verify_password
from fastapi.security import OAuth2PasswordRequestForm


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def authenticate_user(
    credentials: schemas.UserCredentials,
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = crud.get_user_by_username(db, credentials.username)
    if not user:
        raise credentials_exception
    if not verify_password(credentials.password, user.hashed_password):
        raise credentials_exception
    return user


def authenticate_user_from_OAuth2(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    credentials = schemas.UserCredentials(
        username=form_data.username, password=form_data.password
    )
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = crud.get_user_by_username(db, credentials.username)
    if not user:
        raise credentials_exception
    if not verify_password(credentials.password, user.hashed_password):
        raise credentials_exception
    return user


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    username = verify_jwt_token(token)
    if username is None:
        raise credentials_exception
    user = crud.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user


def get_post_by_id(
    post_id: int,
    db: Session = Depends(get_db),
):
    post = crud.get_post_by_id(db=db, post_id=post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    return post

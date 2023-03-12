from fastapi import APIRouter, Depends, HTTPException
from .. import dependencies as deps
from .. import schemas
from .. import crud
from .. import security as sec

router = APIRouter(
    tags=["account"],
    responses={
        401: {
            "model": schemas.HTTPError,
            "description": "Wrong login or password",
        },
    },
)

signup_router = APIRouter(
    tags=["account"],
)


@signup_router.post(
    "/signup/",
    response_model=schemas.User,
    responses={
        409: {
            "model": schemas.HTTPError,
            "description": "Username already registered",
        },
    },
)
def sign_up(user: schemas.UserCredentials, db=Depends(deps.get_db)):
    """Register a new account"""
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=409,
            detail="Username already registered",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return crud.create_user(db=db, user=user)


@router.post(
    "/token/",
    response_model=schemas.Token,
)
def login_for_JWT_from_JSON(
    user: schemas.User = Depends(deps.authenticate_user),
):
    """
    Sign in for JWT token with JSON request body.
    Use /tokenform/ when using interactive docs
    """
    access_token = sec.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post(
    "/tokenform/",
    response_model=schemas.Token,
)
def login_for_JWT_from_FORM(
    user: schemas.User = Depends(deps.authenticate_user_from_OAuth2),
):
    """
    Sign in for JWT token with Post Form
    This method is preferred when using interactive docs
    """
    access_token = sec.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.put(
    "/edit/",
    response_model=schemas.User,
)
def update_credentials(
    new_credentials: schemas.UserCredentials,
    db=Depends(deps.get_db),
    user: schemas.User = Depends(deps.authenticate_user),
):
    """Update your username or/and password"""
    user = crud.update_user(db, user, new_credentials)
    return user


@router.delete(
    "/delete/",
    response_model=schemas.Success,
)
def delete_account(
    db=Depends(deps.get_db),
    user: schemas.User = Depends(deps.authenticate_user),
):
    """Delete your account, your reactions, your posts and reactions to them"""
    crud.delete_user(db, user)
    return schemas.Success(result="Success")


@router.get(
    "/me/",
    response_model=schemas.User,
    responses={
        401: {
            "model": schemas.HTTPError,
            "description": "Unauthorized",
        },
    },
)
def get_current_user(
    db=Depends(deps.get_db), current_user=Depends(deps.get_current_user)
):
    """Your user profile"""
    db_user = crud.get_user(db, user_id=current_user.id)
    return db_user

from fastapi import APIRouter, Depends, HTTPException
from .. import dependencies as deps
from .. import schemas
from .. import crud

router = APIRouter(
    tags=["users"],
)


@router.get("/", response_model=list[schemas.User])
def list_users(
    pagination_params=Depends(schemas.PaginationParams), db=Depends(deps.get_db)
):
    """Get users"""
    users = crud.get_users(
        db, skip=pagination_params.skip, limit=pagination_params.limit
    )
    return users


@router.get(
    "/{user_id}/",
    response_model=schemas.User,
    responses={
        404: {
            "model": schemas.HTTPError,
            "description": "User not found",
        },
    },
)
def get_user(user_id: int, db=Depends(deps.get_db)):
    """Get user by id"""
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    return db_user

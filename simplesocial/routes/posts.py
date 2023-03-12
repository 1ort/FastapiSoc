from fastapi import APIRouter, Depends, HTTPException

from simplesocial import crud
from simplesocial import dependencies as deps
from simplesocial import models, schemas

manage_post_router = APIRouter(
    tags=["posts"],
    responses={
        404: {
            "model": schemas.HTTPError,
            "description": "Item not found",
        },
        403: {
            "model": schemas.HTTPError,
            "description": "Forbidden",
        },
        401: {
            "model": schemas.HTTPError,
            "description": "Unauthorized",
        },
    },
)


router = APIRouter(tags=["posts"])


@router.get(
    "/",
    response_model=list[schemas.Post],
)
async def post_feed(
    pagination_params=Depends(schemas.PaginationParams), db=Depends(deps.get_db)
):
    """Get posts"""
    posts = crud.get_posts(
        db, skip=pagination_params.skip, limit=pagination_params.limit
    )
    return posts


@router.get(
    "/{post_id}/",
    response_model=schemas.Post,
    responses={
        404: {
            "model": schemas.HTTPError,
            "description": "Post not found",
        },
    },
)
async def get_single_post(post=Depends(deps.get_post_by_id), db=Depends(deps.get_db)):
    """Get single post by id"""
    return post


@router.post(
    "/new/",
    response_model=schemas.Post,
    responses={
        401: {
            "model": schemas.HTTPError,
            "description": "Unauthorized",
        },
    },
)
async def new_post(
    content: schemas.NewPost,
    db=Depends(deps.get_db),
    current_user=Depends(deps.get_current_user),
):
    """Create new post"""
    post = crud.create_post(db, post=content, user_id=current_user.id)
    return post


@manage_post_router.put(
    "/{post_id}/",
    response_model=schemas.Post,
)
async def edit_post(
    content: schemas.NewPost,
    post=Depends(deps.get_post_by_id),
    db=Depends(deps.get_db),
    current_user=Depends(deps.get_current_user),
):
    """Update content of your post"""
    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Forbidden",
        )
    updated_post = crud.update_post(db, content, post)
    return updated_post


@manage_post_router.delete(
    "/{post_id}/",
    response_model=schemas.Success,
)
async def delete_post(
    post=Depends(deps.get_post_by_id),
    db=Depends(deps.get_db),
    current_user=Depends(deps.get_current_user),
):
    """Delete your post and reactions to it"""
    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Forbidden",
        )
    crud.delete_post(db, post)
    return schemas.Success(result="Success")


@manage_post_router.patch(
    "/{post_id}/like",
    response_model=schemas.Success,
    tags=["reactions"],
)
async def like_post(
    post: models.Post = Depends(deps.get_post_by_id),
    db=Depends(deps.get_db),
    current_user=Depends(deps.get_current_user),
):
    """
    Like someone else's post.
    If you have already disliked this post, the dislike will be replaced with a like.
    You can not like your own posts
    """
    is_like = True
    if post.author_id == current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can't add reactions to your own posts.",
        )
    reacted = crud.add_reaction(db, is_like, post, current_user)
    return (
        schemas.Success(result="Success")
        if reacted
        else schemas.Success(result="Alredy liked")
    )


@manage_post_router.patch(
    "/{post_id}/dislike",
    response_model=schemas.Success,
    tags=["reactions"],
)
async def dislike_post(
    post=Depends(deps.get_post_by_id),
    db=Depends(deps.get_db),
    current_user=Depends(deps.get_current_user),
):
    """
    Dislike someone else's post.
    If you have already liked this post, the like will be replaced with a dislike.
    You can not dislike your own posts
    """
    is_like = False
    if post.author_id == current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can't add reactions to your own posts.",
        )
    reacted = crud.add_reaction(db, is_like, post, current_user)
    return (
        schemas.Success(result="Success")
        if reacted
        else schemas.Success(result="Alredy disliked")
    )


@manage_post_router.patch(
    "/{post_id}/cancel",
    response_model=schemas.Success,
    tags=["reactions"],
)
async def remove_reaction(
    post=Depends(deps.get_post_by_id),
    db=Depends(deps.get_db),
    current_user=Depends(deps.get_current_user),
):
    """Delete your reaction to someone else's post"""
    reaction = crud.get_reaction(db, post, current_user)
    if reaction is None:
        raise HTTPException(
            status_code=404,
            detail="Reaction not found",
        )
    crud.delete_reaction(db, reaction)
    return schemas.Success(result="Success")

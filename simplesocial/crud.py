from sqlalchemy.orm import Session

from . import models, schemas, reaction_cache
from .security import get_password_hash

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCredentials):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user: models.User, NewCreds: schemas.UserCredentials):
    hashed_password = get_password_hash(NewCreds.password)
    user.hashed_password = hashed_password
    user.username = NewCreds.username
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user: models.User):
    db.delete(user)
    db.commit()


def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Post)
        .order_by(models.Post.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_post_by_id(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()


def create_post(db: Session, post: schemas.NewPost, user_id: int):
    db_post = models.Post(**post.dict(), author_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def update_post(db: Session, content: schemas.NewPost, post: models.Post):
    for key, value in content.dict().items():
        setattr(post, key, value)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def delete_post(db: Session, post: models.Post):
    db.delete(post)
    db.commit()

@reaction_cache.update_reaction_cache
def add_reaction(
    db: Session, is_like: bool, post: models.Post, user: models.User
) -> models.Reaction | None:
    reaction = get_reaction(db, post, user)
    if reaction is None:
        reaction = models.Reaction(from_id=user.id, post_id=post.id, is_like=is_like)
        db.add(reaction)
        db.commit()
        db.refresh(reaction)
        return reaction

    if reaction.is_like != is_like:
        return update_reaction(db, reaction, is_like)
    return None  # If user's previous reaction is same

@reaction_cache.update_reaction_cache
def update_reaction(
    db: Session, reaction: models.Reaction, is_like: bool
) -> models.Reaction:
    reaction.is_like = is_like
    db.add(reaction)
    db.commit()
    db.refresh(reaction)
    return reaction

@reaction_cache.get_from_cache
def get_reaction(db: Session, post: models.Post, user: models.User):
    return (
        db.query(models.Reaction)
        .filter(models.Reaction.post == post)
        .filter(models.Reaction.user == user)
        .first()
    )

@reaction_cache.delete_from_cache
def delete_reaction(db: Session, reaction: models.Reaction):
    db.delete(reaction)
    db.commit()

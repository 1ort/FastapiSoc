from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Boolean,
    UniqueConstraint,
    func,
    select,
)
from sqlalchemy.orm import relationship, object_session
from .reaction_cache import cached_reactions_count


from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    posts = relationship(
        "Post",
        back_populates="author",
        cascade="all, delete-orphan",
    )
    reactions = relationship(
        "Reaction",
        back_populates="user",
        cascade="all, delete-orphan",
    )


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    content = Column(String)
    author_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User", back_populates="posts")
    reactions = relationship(
        "Reaction", back_populates="post", cascade="all, delete-orphan"
    )

    @property
    @cached_reactions_count
    def reactions_count(self):
        likes = object_session(self).scalar(
            select(func.count(Reaction.id)).where(
                Reaction.post_id == self.id, Reaction.is_like
            )
        )
        dislikes = object_session(self).scalar(
            select(func.count(Reaction.id)).where(
                Reaction.post_id == self.id, Reaction.is_like == False
            )
        )
        return {"likes": likes, "dislikes": dislikes}


class Reaction(Base):
    __tablename__ = "reactions"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    from_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    is_like = Column(Boolean)
    __table_args__ = (UniqueConstraint("from_id", "post_id", name="from_to"),)
    user = relationship("User", back_populates="reactions")
    post = relationship("Post", back_populates="reactions")

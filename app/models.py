from .database import Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, INTEGER, String, TIMESTAMP, BIGINT, BOOLEAN, text, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "posts"

    id = Column(INTEGER, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(String(255), nullable=False)
    published = (Column(BOOLEAN, server_default=text("True")))
    created_at = Column(TIMESTAMP, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP"))

    owner_id = Column(INTEGER, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")


class User(Base):
    __tablename__ = "users"
    id = Column(INTEGER, primary_key=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP"))


class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(INTEGER, ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True)

    post_id = Column(INTEGER, ForeignKey(
        "posts.id", ondelete="CASCADE"), primary_key=True)

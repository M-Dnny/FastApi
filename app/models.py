from enum import unique
from pickle import FALSE
from .database import Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean, Column, INTEGER, Integer, String, TIMESTAMP, BIGINT, BOOLEAN, text, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    fullname = Column(String)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    image_path = Column(String)
    image_url = Column(String)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    phone_number = Column(Integer, nullable=FALSE)


class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey(
        "posts.id", ondelete="CASCADE"), primary_key=True)


class Profile(Base):
    __tablename__ = "profile"
    id = Column(Integer, primary_key=True, nullable=False)
    image_path = Column(String)
    image_url = Column(String)

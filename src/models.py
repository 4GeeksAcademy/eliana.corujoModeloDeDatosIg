from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List  # Necesario para las relaciones (List["Post"])
import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False) # Aumentado el tamaño por si guardas un hash
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=True)

    posts: Mapped[List["Post"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    comments: Mapped[List["Comment"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    likes: Mapped[List["Like"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            # do not serialize the password, its a security breach
        }
class Post(db.Model):
    __tablename__ = 'post'
    id: Mapped[int] = mapped_column(primary_key=True)
    image_url: Mapped[str] = mapped_column(String(255), nullable=False)
    caption: Mapped[str] = mapped_column(String(500), nullable=True) # El texto del post
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)    
    user: Mapped["User"] = relationship(back_populates="posts")
    comments: Mapped[List["Comment"]] = relationship(back_populates="post", cascade="all, delete-orphan")
    likes: Mapped[List["Like"]] = relationship(back_populates="post", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "image_url": self.image_url,
            "caption": self.caption,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
            "likes_count": len(self.likes) # Un dato útil derivado
        }
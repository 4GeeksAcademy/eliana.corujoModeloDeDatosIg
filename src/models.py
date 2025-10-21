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
    password: Mapped[str] = mapped_column(String(250), nullable=False) 
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
class Comment(db.Model):
    __tablename__ = 'comment'
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(500), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)
    user: Mapped["User"] = relationship(back_populates="comments")
    post: Mapped["Post"] = relationship(back_populates="comments")
    def serialize(self):
        return {
            "id": self.id,
            "text": self.text,
            "user_id": self.user_id,
            "post_id": self.post_id
        }
class Like(db.Model):
    __tablename__ = 'like'
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now)
    user: Mapped["User"] = relationship(back_populates="likes")
    post: Mapped["Post"] = relationship(back_populates="likes")

    def serialize(self):
        return {
            "user_id": self.user_id,
            "post_id": self.post_id,
            "created_at": self.created_at.isoformat()
         }
if __name__ == "__main__":
    from eralchemy2 import render_er
    import os
    if not isinstance(db, SQLAlchemy):
        raise ValueError("La variable 'db' no es una instancia de SQLAlchemy. Asegúrate de que esté definida.")

    try:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        diagram_path = os.path.join(dir_path, '..', 'diagram.png')
        render_er(db.Model, diagram_path)
        print(f"Diagrama '{diagram_path}' generado exitosamente.")
    except Exception as e:
            print(f"Error generando diagrama: {e}")
            print("Asegúrate de tener 'eralchemy2' y 'graphviz' instalados.")
            print("Instala graphviz (ej: 'apt-get install graphviz' o 'brew install graphviz')")
            print("Y luego 'pip install eralchemy2'")

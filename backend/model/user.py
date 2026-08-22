from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Date, Enum as sqlalchemyEnum, func, DateTime, Integer
from typing import List, Optional
from datetime import datetime
from model.base import Base
from model.task import Task
from db import db

class User(db.Model):
  __tablename__ = 'users'
  
  id: Mapped[int] = mapped_column(primary_key=True)
  first_name: Mapped[str] = mapped_column(String(30))
  last_name: Mapped[str] = mapped_column(String(30))
  email: Mapped[str] = mapped_column(String(50), unique=True)
  password_hash: Mapped[str] = mapped_column(String(255)) # Hashed password
  
  created_at: Mapped[datetime] = mapped_column(server_default=func.now())
  updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
  
  tasks: Mapped[List["Task"]] = relationship(back_populates='user', cascade='all, delete-orphan')
  
  def __repr__(self) -> str:
    return f"User(id={self.id!r}, email={self.email}, fullname={self.first_name+" "+self.last_name!r})"
  
  def to_dict(self) -> str:
    return {
            "id": self.id,
            "full name": self.first_name + " "+ self.last_name,
            "email": self.email,
            "tasks": self.tasks
            }
  
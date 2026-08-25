from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, func, Enum as SAEnum
from typing import List
import enum
from datetime import datetime
# from model.task import Task
from model.base import Base
from app.extensions import bcrypt

class UserRole(enum.Enum):
  USER = 'user'
  ADMIN = 'admin'
  MODERATOR = 'moderator' # only use for specific ppl
  
class User(Base):
  __tablename__ = 'users'
  
  id: Mapped[int] = mapped_column(primary_key=True)
  first_name: Mapped[str] = mapped_column(String(30))
  last_name: Mapped[str] = mapped_column(String(30))
  email: Mapped[str] = mapped_column(String(50), unique=True)
  password: Mapped[str] = mapped_column(String(255)) # Hashed password
  role: Mapped[UserRole] = mapped_column(SAEnum(UserRole, valuescallable=lambda x: [e.value for e in x]), default=UserRole.USER)
  
  created_at: Mapped[datetime] = mapped_column(server_default=func.now())
  updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
  
  task: Mapped[List["Task"]] = relationship(back_populates='user', cascade='all, delete-orphan')
  
  def check_password(self, password):
    return bcrypt.check_password_hash(self.password, password)
  
  def is_admin(self):
    return self.role == UserRole.ADMIN
  
  def is_mod(self):
    return self.role == UserRole.MODERATOR
  
  def __repr__(self) -> str:
    return f"User(id={self.id!r}, email={self.email}, fullname={self.first_name} {self.last_name})"
  
  def to_dict(self) -> dict:
    return {
            "id": self.id,
            "full_name": f"{self.first_name} {self.last_name}",
            "email": self.email,
            "role": self.role.value,
            "tasks": [t.to_dict() for t in self.task] if self.task else []
            }
  
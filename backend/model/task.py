from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Enum as sqlalchemyEnum, func, DateTime
from typing import Optional
from datetime import datetime
import enum
from model.user import User
from db import db

class TaskPriority(enum.Enum):
  HIGH = 'high'
  MEDIUM = 'medium'
  LOW = 'low'
  
  @classmethod
  def choices(cls):
    return [priority.value for priority in cls]
  
class TaskStatus(enum.Enum):
  PENDING = 'pending'
  IN_PROGRESS = 'in_progress'
  COMPLETED = 'completed'
  
  @classmethod
  def choices(cls):
    return [status.value for status in cls]

'''
task - id, title, duration, created_at, priority
'''

class Task(db.Model):
  __tablename__ = 'tasks'
  id: Mapped[int] = mapped_column(primary_key=True)
  title: Mapped[str] = mapped_column(String(100))
  priority: Mapped[TaskPriority] = mapped_column(sqlalchemyEnum(TaskPriority), default=TaskPriority.MEDIUM)
  status: Mapped[TaskStatus] = mapped_column(sqlalchemyEnum(TaskStatus), default=TaskStatus.PENDING)
  
  start_time: Mapped[Optional[datetime]] = mapped_column(DateTime(), nullable=True)
  end_time: Mapped[Optional[datetime]] = mapped_column(DateTime(), nullable=True)
  
  created_at: Mapped[datetime] = mapped_column(server_default=func.now())
  updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
  completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(), nullable=True)
  
  user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
  user: Mapped['User'] = relationship(back_populates='tasks')
  
  def __repr__(self) -> str:
    duration_str = f" duration=({self.computed_duration()})" if self.computed_duration() else ""
    return f"id=({self.id}), title={self.title} priority={self.priority}{duration_str} {self.status.value}"
    
  @property
  def computed_duration(self) -> Optional[int]:
    if self.start_time and self.end_time:
      return int((self.end_time - self.start_time).total_seconds())
    return None

  @property
  def is_complete(self):
    return self.status == TaskStatus.COMPLETED

  def to_dict(self):
    return {
          "id": self.id,
          "title": f"{self.title}",
          "priority": self.priority.value,
          "status": self.status.value,
          "duration": self.computed_duration() if self.start_time and self.end_time else None,
          "created_at": self.created_at
        }

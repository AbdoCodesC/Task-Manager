from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Enum as SAEnum, DateTime, Text, UUID
from typing import Optional
from datetime import datetime, timezone
import uuid
import enum

# from model.user import User
from model.base import Base

class TaskPriority(str, enum.Enum):
  LOW = "low"
  MEDIUM = "medium"
  HIGH = "high"
  URGENT = "urgent"
  
class TaskStatus(str, enum.Enum):
  TODO = "todo"
  IN_PROGRESS = "in_progress"
  DONE = "done"
  ARCHIVED = "archived"
  
class Task(Base):
  __tablename__ = 'tasks'
  id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  title: Mapped[str] = mapped_column(String(100), nullable=False)
  description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
  priority: Mapped[TaskPriority] = mapped_column(SAEnum(TaskPriority), default=TaskPriority.MEDIUM, nullable=False)
  status: Mapped[TaskStatus] = mapped_column(SAEnum(TaskStatus), default=TaskStatus.TODO, nullable=False)
  
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
  updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
  completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
  
  # FK
  project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('projects.id'), nullable=False)
  
  # 
  project: Mapped['Project'] = relationship(back_populates='tasks')
  time_blocks: Mapped[list['TimeBlock']] = relationship(back_populates='task', cascade='all, delete-orphan')
  comments: Mapped[list['Comment']] = relationship(back_populates='task', cascade='all, delete-orphan')
  activities: Mapped[list['TaskActivity']] = relationship(back_populates='task', cascade='all, delete-orphan')
  
  def __repr__(self) -> str:
    return f"id=({self.id}), title={self.title} priority={self.priority} {self.status.value}"

  @property
  def is_complete(self):
    return self.status == TaskStatus.DONE

  def to_dict(self) -> dict:
    return {
      "id": str(self.id),
      "title": self.title,
      "description": self.description,
      "priority": self.priority.value,
      "status": self.status.value,
      "created_at": self.created_at,
      'completed_at': self.completed_at.isoformat() if self.completed_at else None,
      "project_id": str(self.project_id)
    }

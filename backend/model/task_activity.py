import uuid
import enum
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import UUID, DateTime, ForeignKey, JSON, String, Text, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.base import Base


class ActivityType(str, enum.Enum):
  CREATED = 'created'
  UPDATED = 'updated'
  STATUS_CHANGED = 'status_changed'
  COMPLETED = 'completed'
  REOPENED = 'reopened'
  PRIORITY_CHANGED = 'priority_changed'
  ASSIGNED = 'assigned'
  COMMENTED = 'commented'
  TIME_BLOCK_ADDED = 'time_block_added'
  DELETED = 'deleted'

class TaskActivity(Base):
  __tablename__ = 'task_activities'
  
  id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  task_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('tasks.id', ondelete='CASCADE'), nullable=False)
  user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
  activity_type: Mapped[ActivityType] = mapped_column(SAEnum(ActivityType), nullable=False)
  field_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
  old_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
  new_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
  details: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
  
  task: Mapped['Task'] = relationship(back_populates='activities')
  user: Mapped['User'] = relationship(back_populates='activities')
  
  def to_dict(self):
    return {
      "id": str(self.id),
      "task_id": str(self.task_id),
      "user_id": str(self.user_id),
      "activity_type": self.activity_type.value,
      "field_name": self.field_name,
      "old_value": self.old_value,
      "new_value": self.new_value,
      "details": self.details,
      "created_at": self.created_at.isoformat(),
    }
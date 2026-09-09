from model.base import Base
import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID, ForeignKey, String, DateTime
from datetime import datetime, timezone

class Comment(Base):
  __tablename__ = 'comments'
  
  id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  message: Mapped[str] = mapped_column(String(255), nullable=False)
  task_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('tasks.id'), nullable=False)
  user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
  
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
  updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
  task: Mapped['Task'] = relationship(back_populates='comments')
  user: Mapped['User'] = relationship()
  
  def to_dict(self):
    return {
      "id": self.id,
      "message": self.message,
      "task_id": self.task_id,
      "user_id": self.user_id,
      "created_at": self.created_at
    }
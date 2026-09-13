import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID, String, ForeignKey, Text, Enum as SAEnum, DateTime, UniqueConstraint
from model.base import Base
from typing import Optional
import enum

class ProjectStatus(enum.Enum):
  TODO = 'todo'
  IN_PROGRESS = 'in_progress'
  COMPLETED = 'completed'

class Project(Base):
  __tablename__ = 'projects'
  __table_args__ = (UniqueConstraint('workspace_id', 'name'),)
  
  id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  name: Mapped[str] = mapped_column(String(100), nullable=False)
  description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
  status: Mapped[ProjectStatus] = mapped_column(SAEnum(ProjectStatus), default=ProjectStatus.TODO)
  
  created_at: Mapped[datetime]  = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
  updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
  
  workspace_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('workspaces.id'), nullable=False)
  workspace: Mapped['Workspace'] = relationship(back_populates='projects')
  tasks: Mapped[list['Task']] = relationship(back_populates='project', cascade='all, delete-orphan')

  def __repr__(self):
    return f'id: {self.id} name: {self.name} status: {self.status} workspace_id: {self.workspace_id}'
  
  def to_dict(self):
    return {
        "id": str(self.id),
        "name": self.name,
        "description": self.description,
        "status": self.status.value,
        "workspace_id": str(self.workspace_id),
    }
  
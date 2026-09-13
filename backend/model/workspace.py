from model.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID, ForeignKey, String, DateTime
import uuid
from datetime import datetime, timezone

class Workspace(Base):
  __tablename__ = 'workspaces'
  
  id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  name: Mapped[str] = mapped_column(String(100), nullable=False)
  slug: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
  
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
  updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
  
  # FK - SOURCE OF TRUTH
  owner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
  
  # 1:N
  owner: Mapped['User'] = relationship(back_populates='owned_workspaces')
  member_records: Mapped[list['WorkspaceMember']] = relationship(back_populates='workspace', cascade='all, delete-orphan')
  projects: Mapped[list['Project']] = relationship(back_populates='workspace', cascade='all, delete-orphan')
  invitations: Mapped[list['WorkspaceInvitation']] = relationship(back_populates='workspace', cascade='all, delete-orphan')
  
  
  def __repr__(self) -> str:
    return f'id: {self.id} name: {self.name} owner_id: {self.owner_id}'
  
  def to_dict(self) -> dict:
    return {
      'id': str(self.id),
      'name': self.name,
      'slug': self.slug,
      'owner_id': str(self.owner_id),
    }
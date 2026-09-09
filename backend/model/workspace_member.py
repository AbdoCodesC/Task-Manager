from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import datetime, timezone
from sqlalchemy import UUID, DateTime, ForeignKey, Enum as SAEnum, UniqueConstraint
from model.base import Base
import uuid
import enum

class MemberRole(enum.Enum):
  OWNER = 'owner'
  ADMIN = 'admin'
  MEMBER = 'member'

class WorkspaceMember(Base):
  __tablename__ = 'workspace_members'
  __table_args__ = (UniqueConstraint("user_id", "workspace_id"),)
  
  id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  role: Mapped[MemberRole] = mapped_column(SAEnum(MemberRole, values_callable=lambda x: [e.value for e in x]), default=MemberRole.MEMBER, nullable=False)
  joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

  user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
  workspace_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('workspaces.id'), nullable=False)
  
  user: Mapped['User'] = relationship(back_populates='workspace_memberships')
  workspace: Mapped['Workspace'] = relationship(back_populates='member_records')
  

  def is_admin(self):
    return self.role == MemberRole.ADMIN
    
  def is_owner(self):
    return self.role == MemberRole.OWNER
  
  def to_dict(self) -> dict:
    return {
      'id': self.id,
      'role': self.role,
      'user_id': self.user_id,
      "workspace_id": self.workspace_id,
      "joined_at": self.joined_at
    }
  
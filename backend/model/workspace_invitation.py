import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID, String, ForeignKey, Enum as SAEnum, DateTime, UniqueConstraint
from typing import Optional
from model.base import Base
import enum

class InvitationStatus(str, enum.Enum):
  PENDING = 'pending'
  ACCEPTED = 'accepted'
  DECLINED = 'declined'
  EXPIRED = 'expired'
  CANCELLED = 'cancelled'

class WorkspaceRole(str, enum.Enum):
  MEMBER = 'member'
  ADMIN = 'admin'
  OWNER = 'owner'

class WorkspaceInvitation(Base):
  __tablename__ = 'workspace_invitations'
  __table_args__ = (UniqueConstraint("workspace_id", "email"),)
  
  id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  email: Mapped[str] = mapped_column(String(100), nullable=False)
  role: Mapped[WorkspaceRole] = mapped_column(SAEnum(WorkspaceRole, name='workspace_role'), default=WorkspaceRole.MEMBER, nullable=False)
  status: Mapped[InvitationStatus] = mapped_column(SAEnum(InvitationStatus, name='invitation_status'), default=InvitationStatus.PENDING, nullable=False)
  token: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)
  
  expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
  accepted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
  
  workspace_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('workspaces.id'), nullable=False)
  invited_by_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

  invited_by: Mapped['User'] = relationship(back_populates="sent_invitations")
  workspace: Mapped['Workspace'] = relationship(back_populates='invitations')
  
  
  def to_dict(self) -> dict:
    return {
      'id': str(self.id),
      'role': self.role.value,
      'invited_by_id': str(self.invited_by_id),
      "workspace_id": str(self.workspace_id),
      "email": self.email,
      "status": self.status.value,
      "token": str(self.token),
      "expires_at": self.expires_at,
      "accepted_at": self.accepted_at
    }

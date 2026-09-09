from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from sqlalchemy import String, UUID, DateTime
from datetime import datetime, timezone
# from model.task import Task
from model.base import Base
from app.extensions import bcrypt


class User(Base):
  __tablename__ = 'users'
  
  id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  first_name: Mapped[str] = mapped_column(String(30))
  last_name: Mapped[str] = mapped_column(String(30))
  email: Mapped[str] = mapped_column(String(100), unique=True)
  password_hash: Mapped[str] = mapped_column(String(255)) # Hashed password
  
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
  updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
  
  owned_workspaces: Mapped[list["Workspace"]] = relationship(back_populates='owner')
  workspace_memberships: Mapped[list['WorkspaceMember']] = relationship(back_populates='user', cascade='all, delete-orphan')

  sent_invitations: Mapped[list['WorkspaceInvitation']] = relationship(back_populates="invited_by")
  activities: Mapped[list['TaskActivity']] = relationship(back_populates='user')
    
  def check_password(self, password):
    return bcrypt.check_password_hash(self.password_hash, password)
  
  def __repr__(self) -> str:
    return f"User(id={self.id!r}, email={self.email}, fullname={self.first_name} {self.last_name})"
  
  def to_dict(self) -> dict:
    return {
            "id": self.id,
            "full_name": f"{self.first_name} {self.last_name}",
            "email": self.email,
            }
  
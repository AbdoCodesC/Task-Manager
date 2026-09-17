from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from sqlalchemy import String, UUID, DateTime, Boolean, Enum as SAEnum, Integer
from datetime import datetime, timezone
# from model.task import Task
from model.base import Base
from app.extensions import bcrypt
import enum
from typing import Optional

class AccountStatus(str, enum.Enum):
  ACTIVE = 'active'
  SUSPENDED = 'suspended'
  DELETED = 'deleted'

class UserRole(str, enum.Enum):
  USER = 'user'
  ADMIN = 'admin'

class User(Base):
  __tablename__ = 'users'

  id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  first_name: Mapped[str] = mapped_column(String(30), nullable=False)
  last_name: Mapped[str] = mapped_column(String(30), nullable=False)
  email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
  password_hash: Mapped[str] = mapped_column(String(255), nullable=False) # Hashed password
  email_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
  token_version: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

  account_status: Mapped[AccountStatus] = mapped_column(SAEnum(AccountStatus, name="account_status", values_callable=lambda enum_class: [member.value for member in enum_class],), default=AccountStatus.ACTIVE, nullable=False)
  role: Mapped[UserRole] = mapped_column(SAEnum(UserRole, name='user_role', values_callable=lambda enum_class: [member.value for member in enum_class]), default=UserRole.USER, nullable=False)

  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
  updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
  deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

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
      "id": str(self.id),
      "full_name": f"{self.first_name} {self.last_name}",
      "email": self.email,
      "created_at": self.created_at,
      'account_status': self.account_status.value,
      'role': self.role.value,
      }

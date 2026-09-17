from db import db
from model.workspace_invitation import WorkspaceInvitation, WorkspaceRole, InvitationStatus
from marshmallow import ValidationError
from model.workspace_member import WorkspaceMember, MemberRole
from schema import workspace_invitation_schema, workspace_member_update_schema
from datetime import datetime, timezone, timedelta
import uuid
from utils.workspace_member_helpers import get_workspace_membership

class WorkspaceInvitationServiceError(Exception):
  status_code = 400

class NotFound(WorkspaceInvitationServiceError):
  status_code = 404
  
class Unauthorized(WorkspaceInvitationServiceError):
  status_code = 403
  
#  Workspace invitations
  
def get_workspace_invitations(workspace_id, user):
  membership = get_workspace_membership(workspace_id, user)
  if membership.role not in [MemberRole.OWNER, MemberRole.ADMIN]:
    raise Unauthorized('You do not have permission to view invitations')
  
  invitations = db.session.scalars(db.select(WorkspaceInvitation).where(WorkspaceInvitation.workspace_id == workspace_id).order_by(WorkspaceInvitation.created_at.desc())).all()
  
  return invitations

def create_workspace_invitation(workspace_id, user, data):
  if not data:
    raise WorkspaceInvitationServiceError('Data not provided')
    
  membership = get_workspace_membership(workspace_id, user)
  if membership.role != MemberRole.OWNER:
    raise Unauthorized('You do not have permission to create invitations')  

  email = (data.get('email') or '').strip()
  try:
    role = WorkspaceRole(data['role'])
  except ValueError as e:
    raise WorkspaceInvitationServiceError('Role needs to be (member, owner, or admin)')
  status = InvitationStatus.PENDING
  token = uuid.uuid4()
  expires_at = datetime.now(timezone.utc) + timedelta(days=1) # one day 
  
  errors = workspace_invitation_schema.validate({'email': email, 'role': role, 'status': status, 'token': token, 'expires_at': expires_at})
  if errors:
    raise ValidationError(errors)
  
  invitation = WorkspaceInvitation(email=email, role=role, status=status, token=token, expires_at=expires_at, workspace_id=workspace_id, invited_by_id=user.id)
  
  db.session.add(invitation)
  db.session.commit()
  
  return invitation

def delete_workspace_invitation(workspace_id, invitation_id, user):
  membership = get_workspace_membership(workspace_id, user)
  if membership.role != MemberRole.OWNER:
    raise Unauthorized('You do not have permission to delete invitations')  
  
  invitation = db.session.scalar(db.select(WorkspaceInvitation).where(WorkspaceInvitation.workspace_id == workspace_id, WorkspaceInvitation.id == invitation_id))
  if not invitation:
    raise NotFound('Invitation not found or you do not belong to this workspace')
  
  db.session.delete(invitation)
  db.session.commit()

# Accept / Decline

def accept_invitation(token, user):
  if not user or not user.id:
    raise Unauthorized("User not authorized")
  
  invitation = db.session.scalar(db.select(WorkspaceInvitation).where(WorkspaceInvitation.token == token))
  if not invitation:
    raise NotFound('Invitation not found')
  
  if invitation.status == InvitationStatus.ACCEPTED:
    raise WorkspaceInvitationServiceError('You already accepted this invitation')
  if invitation.expires_at <= datetime.now(timezone.utc):
    invitation.status = InvitationStatus.EXPIRED
    db.session.commit()
    raise WorkspaceInvitationServiceError('This invitation has expired')
  if invitation.status == InvitationStatus.DECLINED:
    raise WorkspaceInvitationServiceError('The invitation was already declined')
  if invitation.status == InvitationStatus.CANCELLED:
    raise WorkspaceInvitationServiceError('This invitation was cancelled')

  if invitation.email.lower() != user.email.lower():
    raise Unauthorized('This invitation was sent to a different email address')
  
  workspace_id = invitation.workspace_id
  if not workspace_id:
    raise NotFound('Workspace not found')
  
  existing_member = db.session.scalar(db.select(WorkspaceMember).where(WorkspaceMember.user_id == user.id, WorkspaceMember.workspace_id == workspace_id))
  if existing_member:
    raise WorkspaceInvitationServiceError('You are already a member of this workspace')
  
  membership = WorkspaceMember(user_id=user.id, workspace_id=workspace_id, role=MemberRole(invitation.role.value))

  invitation.status = InvitationStatus.ACCEPTED
  invitation.accepted_at = datetime.now(timezone.utc)
  
  db.session.add(membership)
  db.session.commit()
  
  return membership
  
def decline_invitation(token, user):
  if not user or not user.id:
    raise Unauthorized("User not authorized")
    
  invitation = db.session.scalar(db.select(WorkspaceInvitation).where(WorkspaceInvitation.token == token))
  if not invitation:
    raise NotFound('Invitation not found')

  if invitation.status == InvitationStatus.ACCEPTED:
    raise WorkspaceInvitationServiceError('You already accepted this invitation')

  if invitation.expires_at <= datetime.now(timezone.utc):
    invitation.status = InvitationStatus.EXPIRED
    db.session.commit()
    raise WorkspaceInvitationServiceError('This invitation has expired')

  if invitation.status == InvitationStatus.DECLINED:
    raise WorkspaceInvitationServiceError('The invitation was already declined')

  if invitation.status == InvitationStatus.CANCELLED:
    raise WorkspaceInvitationServiceError('This invitation was cancelled')

  if invitation.email.lower() != user.email.lower():
    raise Unauthorized('This invitation was sent to a different email address')
  
  workspace_id = invitation.workspace_id
  if not workspace_id:
    raise NotFound('Workspace not found')
  
  existing_member = db.session.scalar(db.select(WorkspaceMember).where(WorkspaceMember.user_id == user.id, WorkspaceMember.workspace_id == workspace_id))
  if existing_member:
    raise WorkspaceInvitationServiceError('You are already a member of this workspace')
  
  invitation.status = InvitationStatus.DECLINED
  
  db.session.commit()
  
  return invitation
      
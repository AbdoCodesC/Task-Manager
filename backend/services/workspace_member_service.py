from db import db
from model.workspace_member import WorkspaceMember, MemberRole
from schema.workspace_member_schema import workspace_member_update_schema
from marshmallow import ValidationError

class WorkspaceMemberServiceError(Exception):
  status_code = 400

class NotFound(WorkspaceMemberServiceError):
  status_code = 404
  
class Unauthorized(WorkspaceMemberServiceError):
  status_code = 403

def get_workspace_membership(workspace_id, user):
  if not user or not user.id:
    raise Unauthorized("User not authorized")

  membership = db.session.scalar(
    db.select(WorkspaceMember).where(
      WorkspaceMember.user_id == user.id,
      WorkspaceMember.workspace_id == workspace_id,
    )
  )

  if not membership:
    raise Unauthorized("Workspace not found or you are not a member")

  return membership

  
def get_members(workspace_id, user):
  get_workspace_membership(workspace_id, user)
  
  members = db.session.scalars(db.select(WorkspaceMember).where(WorkspaceMember.workspace_id == workspace_id).order_by(WorkspaceMember.joined_at.desc())).all()
  
  return members

def update_member(workspace_id, member_id, user, data):
  if not data:
    raise WorkspaceMemberServiceError('No data provided')
  
  membership = get_workspace_membership(workspace_id, user)
  
  if membership.role not in [MemberRole.OWNER, MemberRole.ADMIN]:
    raise Unauthorized("Only the workspace owner can update member roles")
  
  errors = workspace_member_update_schema.validate(data)
  if errors:
    raise ValidationError(errors)
  
  member = db.session.scalar(db.select(WorkspaceMember).where(WorkspaceMember.workspace_id == workspace_id, WorkspaceMember.id == member_id))
  if not member:
    raise NotFound("Workspace member not found")
  
  if member.role == MemberRole.OWNER:
    raise Unauthorized("The workspace owner role cannot be changed")
  
  if 'role' in data:
    try:
      new_role = MemberRole(data["role"])
    except ValueError:
      raise WorkspaceMemberServiceError("Invalid member role")

    if member.role == MemberRole.OWNER:
      raise Unauthorized("The workspace owner role cannot be changed")

    if new_role == MemberRole.OWNER:
      raise Unauthorized("The owner role cannot be assigned")

    member.role = new_role
  
  db.session.commit()
  
  return member

def delete_member(workspace_id, member_id, user):
  membership = get_workspace_membership(workspace_id, user)
  
  if membership.role not in [MemberRole.OWNER, MemberRole.ADMIN]:
    raise Unauthorized('You do not have permission to delete members')
  
  member = db.session.scalar(db.select(WorkspaceMember).where(WorkspaceMember.workspace_id == workspace_id, WorkspaceMember.id == member_id))
  if not member:
    raise NotFound("Workspace member not found")
  
  if member.role == MemberRole.OWNER:
    raise Unauthorized("The workspace owner cannot be removed")
  
  db.session.delete(member)
  db.session.commit()



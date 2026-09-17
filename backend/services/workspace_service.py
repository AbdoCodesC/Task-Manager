from db import db
from model.workspace_member import WorkspaceMember, MemberRole
from model.workspace import Workspace
from schema.workspace_schema import workspace_schema, workspace_update_schema
from utils.workspace_helpers import create_slug
from marshmallow import ValidationError

class WorkspaceServiceError(Exception):
  status_code = 400

class Unauthorized(WorkspaceServiceError):
  status_code = 403

class NotFound(WorkspaceServiceError):
  status_code = 404
  
def get_workspaces(user):
  if not user or not user.id:
    raise Unauthorized('User not authorized')  
  
  # get all workspaces that this user belongs to!
  workspaces = db.session.scalars(db.select(Workspace).join(WorkspaceMember).where(WorkspaceMember.user_id == user.id)).all()
  
  return workspaces

def get_workspace(workspace_id, user):
  if not workspace_id:
    raise WorkspaceServiceError("Workspace ID is required to fetch a workspace")
  if not user or not user.id:
    raise Unauthorized('User not authorized')  
  
  # get workspace that this user belongs to!
  workspace = db.session.scalar(db.select(Workspace).join(WorkspaceMember).where(WorkspaceMember.user_id == user.id, WorkspaceMember.workspace_id == workspace_id))
  if not workspace:
    raise NotFound("Workspace not found or you are not a member")
  
  return workspace

def create_workspace(user, data, commit=True):
  if not user or not user.id:
    raise Unauthorized('User not authorized')  
  
  name = (data.get('name') or '').strip()
  if not name:
    raise WorkspaceServiceError('Name field required')
  
  slug = create_slug(name)
  
  errors = workspace_schema.validate({'name': name, 'slug': slug, 'owner_id': user.id})
  if errors:
    raise ValidationError(str(errors))
  
  workspace = Workspace(name=name, slug=slug, owner_id=user.id)
  db.session.add(workspace)
  db.session.flush()
  
  workspace_member = WorkspaceMember(user_id=user.id, workspace_id=workspace.id, role=MemberRole.OWNER)
  db.session.add(workspace_member)  
  
  if commit:
    db.session.commit()
  
  return workspace

def update_workspace(workspace_id, user, data):
  if not workspace_id:
    raise WorkspaceServiceError("Workspace ID is required to update a workspace")
  
  if not user or not user.id:
    raise Unauthorized('User not authorized')
  
  new_name = (data.get('name') or '').strip()
  if not new_name:
    raise WorkspaceServiceError('Name field required')
  
  new_slug = create_slug(new_name)
  
  errors = workspace_update_schema.validate({"name": new_name, 'slug': new_slug})
  if errors:
    raise ValidationError(errors)
  
  member = db.session.scalar(db.select(WorkspaceMember).where(WorkspaceMember.user_id == user.id, WorkspaceMember.workspace_id == workspace_id))
  if not member:
    raise NotFound("Workspace not found or you are not a member")
  
  if member.role not in [MemberRole.OWNER, MemberRole.ADMIN]:
    raise Unauthorized("You do not have permission to update this workspace")
  
  workspace = db.session.scalar(db.select(Workspace).join(WorkspaceMember).where(WorkspaceMember.user_id == user.id, WorkspaceMember.workspace_id == workspace_id))
  if not workspace: 
    raise NotFound('Workspace not found or you are not a member')
  
  workspace.name = new_name
  workspace.slug = new_slug
  
  db.session.commit()
  
  return workspace

def delete_workspace(workspace_id, user):
  if not workspace_id:
    raise WorkspaceServiceError("Workspace ID is required to delete a workspace")
  
  if not user or not user.id:
    raise Unauthorized('User not authorized')
    
  member = db.session.scalar(db.select(WorkspaceMember).where(WorkspaceMember.user_id == user.id, WorkspaceMember.workspace_id == workspace_id))
  if not member:
    raise NotFound("Workspace not found or you are not a member")
  
  if member.role != MemberRole.OWNER:
    raise Unauthorized('Only the workspace owner can delete this workspace')
  
  workspace = db.session.scalar(db.select(Workspace).join(WorkspaceMember).where(WorkspaceMember.user_id == user.id, WorkspaceMember.workspace_id == workspace_id))
  if not workspace:
    raise NotFound("Workspace not found or you are not a member")
  
  db.session.delete(workspace)
  db.session.commit()

  
  

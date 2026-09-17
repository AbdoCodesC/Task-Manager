from db import db
from model import WorkspaceMember
from services.workspace_member_service import Unauthorized

def get_workspace_membership(workspace_id, user):
  if not user or not user.id:
    raise Unauthorized("User not authorized")
  
  workspace_member = db.session.scalar(db.select(WorkspaceMember).where(WorkspaceMember.user_id == user.id, WorkspaceMember.workspace_id == workspace_id))
  if not workspace_member:
    raise Unauthorized('Workspace not found or you are not a member')
  
  return workspace_member
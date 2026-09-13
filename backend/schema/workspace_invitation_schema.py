from db import db
from app.extensions import ma
from marshmallow_sqlalchemy import SQLAlchemySchema
from model.workspace_invitation import WorkspaceInvitation, WorkspaceRole, InvitationStatus

class WorkspaceInvitationSchema(SQLAlchemySchema):
  class Meta:
    model = WorkspaceInvitation
    load_instance = True
    sqla_session = db.session
    
  id = ma.UUID(dump_only=True)
  email = ma.Email(required=True)
  role = ma.Enum(WorkspaceRole, by_value=True, required=True)
  status = ma.Enum(InvitationStatus, by_value=True, required=True)
  token = ma.UUID(required=True)
  
  expires_at = ma.DateTime(dump_only=True, required=True)
  created_at = ma.DateTime(dump_only=True)
  accepted_at = ma.DateTime(dump_only=True)
  
  workspace_id = ma.UUID(required=True)
  invited_by_id = ma.UUID(required=True)
  
  invited_by = ma.Nested('UserSchema', dump_only=True)
  workspace = ma.Nested('WorkspaceSchema', dump_only=True)
  
  
workspace_invitation_schema = WorkspaceInvitationSchema()
workspace_invitation_update_schema = WorkspaceInvitationSchema(partial=True)
  
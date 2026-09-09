from db import db
from app.extensions import ma
from marshmallow_sqlalchemy import SQLAlchemySchema
from marshmallow.validate import Length
from model.workspace import Workspace

class WorkspaceSchema(SQLAlchemySchema):
  class Meta:
    model = Workspace
    load_instance = True
    sqla_session = db.session
  
  id = ma.UUID(dump_only=True)
  name = ma.Str(validate=Length(min=3, max=100), required=True)
  slug = ma.Str(validate=Length(min=3, max=255), required=True)
  created_at = ma.DateTime(dump_only=True)
  updated_at = ma.DateTime(dump_only=True)
  
  owner_id = ma.UUID(required=True)
  
  owner = ma.Nested('UserSchema', dump_only=True)
  member_records = ma.Nested('WorkspaceMemberSchema', many=True, dump_only=True)
  projects = ma.Nested('ProjectSchema', many=True, dump_only=True)
  invitations = ma.Nested('WorkspaceInvitationSchema', many=True, dump_only=True)
  
workspace_schema = WorkspaceSchema()
workspace_update_schema = WorkspaceSchema(partial=True)
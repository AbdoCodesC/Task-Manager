from db import db
from app.extensions import ma
from marshmallow_sqlalchemy import SQLAlchemySchema
from model.workspace_member import WorkspaceMember, MemberRole

class WorkspaceMemberSchema(SQLAlchemySchema):
  class Meta:
    model = WorkspaceMember
    load_instance = True
    sqla_session = db.session
    
  id = ma.UUID(dump_only=True)
  role = ma.Enum(MemberRole, by_value=True, required=True)
  joined_at = ma.DateTime(dump_only=True)
  
  user_id = ma.UUID(required=True)
  workspace_id = ma.UUID(required=True)
  
  user = ma.Nested('UserSchema', dump_only=True)
  workspace = ma.Nested('WorkspaceSchema', dump_only=True)
  
workspace_member_schema = WorkspaceMemberSchema()
workspace_member_update_schema = WorkspaceMemberSchema(partial=True)
  
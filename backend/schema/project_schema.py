from app.extensions import ma
from marshmallow_sqlalchemy import SQLAlchemySchema
from marshmallow.validate import Length
from model.project import Project, ProjectStatus, ProjectCategory
from db import db

class ProjectSchema(SQLAlchemySchema):
  class Meta:
    model = Project
    load_instance = True
    sqla_session = db.session
    
  id = ma.UUID(dump_only=True)
  name = ma.String(required=True, allow_none=False, validate=Length(min=3, max=100))
  description = ma.String(required=False, allow_none=True)
  status = ma.Enum(ProjectStatus, by_value=True, required=True)
  category = ma.Enum(ProjectCategory, by_value=True, required=True)
  created_at = ma.DateTime(dump_only=True)
  updated_at = ma.DateTime(dump_only=True)
  workspace_id = ma.UUID(dump_only=True)
  
  workspace = ma.Nested('WorkspaceSchema', dump_only=True)
  tasks = ma.Nested('TaskSchema', many=True, dump_only=True)
  
project_schema = ProjectSchema()
project_update_schema = ProjectSchema(partial=True)
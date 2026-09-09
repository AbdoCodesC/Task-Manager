from app.extensions import ma
from model import Task
from model.task import TaskPriority, TaskStatus
from marshmallow_sqlalchemy import SQLAlchemySchema
from marshmallow.validate import Length
from db import db
# from schema import user_schema

class TaskSchema(SQLAlchemySchema):
  class Meta:
    model = Task
    load_instance = True
    sqla_session = db.session
  
  id = ma.UUID(dump_only=True)
  title = ma.String(required=True, validate=Length(min=1, max=100))
  description = ma.String(required=False, allow_none=True, validate=Length(max=1000, error="Reached max character limit for description"))
  priority = ma.Enum(enum=TaskPriority, by_value=True, required=True)
  status = ma.Enum(enum=TaskStatus, by_value=True, required=True)
  
  completed_at = ma.DateTime(required=False, allow_none=True)
  created_at = ma.DateTime(dump_only=True)
  updated_at = ma.DateTime(dump_only=True)
  project_id = ma.UUID(required=True)
  
  project = ma.Nested('ProjectSchema', dump_only=True)
  time_blocks = ma.Nested('TimeBlockSchema', many=True, dump_only=True)
  comments = ma.Nested('CommentSchema', many=True, dump_only=True)
  activities = ma.Nested('TaskActivitySchema', many=True, dump_only=True)

task_schema = TaskSchema()
task_update_schema = TaskSchema(partial=True)

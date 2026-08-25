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
  
  id = ma.Integer(dump_only=True)
  title = ma.String(required=True, validate=Length(min=1, max=100))
  priority = ma.Enum(enum=TaskPriority, by_value=True)
  status = ma.Enum(enum=TaskStatus, by_value=True)
  start_time = ma.DateTime(required=False, allow_none=True)
  end_time = ma.DateTime(required=False, allow_none=True)
  completed_at = ma.DateTime(allow_none=True)
  created_at = ma.DateTime(dump_only=True)
  updated_at = ma.DateTime(dump_only=True)
  user_id = ma.Integer(required=True)
  user = ma.Nested("UserSchema", dump_only=True)

task_schema = TaskSchema()
task_update_schema = TaskSchema(partial=True)

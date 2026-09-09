from db import db
from app.extensions import ma
from marshmallow_sqlalchemy import SQLAlchemySchema
from model.task_activity import TaskActivity, ActivityType

class TaskActivitySchema(SQLAlchemySchema):
  class Meta:
    model = TaskActivity
    load_instance = True
    sqla_session = db.session
  
  id = ma.UUID(dump_only=True)
  task_id = ma.UUID(required=True)
  user_id = ma.UUID(required=True)
  activity_type = ma.Enum(ActivityType, by_value=True, required=True)
  field_name = ma.String(required=False, allow_none=True)
  old_value = ma.String(required=False, allow_none=True)
  new_value = ma.String(required=False, allow_none=True)
  details = ma.Dict(allow_none=True)
  created_at = ma.DateTime(dump_only=True)
  
  task = ma.Nested('TaskSchema', dump_only=True)
  user = ma.Nested('UserSchema', dump_only=True)
  
task_activity_schema = TaskActivitySchema()
task_activity_update_schema = TaskActivitySchema(partial=True)
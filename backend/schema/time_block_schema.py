from db import db
from app.extensions import ma
from marshmallow_sqlalchemy import SQLAlchemySchema
from model.time_block import TimeBlock
from marshmallow.validate import Length

class TimeBlockSchema(SQLAlchemySchema):
  class Meta:
    model = TimeBlock
    load_instance = True
    sqla_session = db.session
  
  id = ma.UUID(dump_only=True)
  title = ma.Str(required=True, validate=Length(min=1, max=100))
  start_time = ma.DateTime(required=False, allow_none=True)
  end_time = ma.DateTime(required=False, allow_none=True)
  
  task_id = ma.UUID(required=True)
  task = ma.Nested('TaskSchema', dump_only=True)
  
time_block_schema = TimeBlockSchema()
time_block_update_schema = TimeBlockSchema(partial=True)
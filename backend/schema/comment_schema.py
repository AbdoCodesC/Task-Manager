from marshmallow_sqlalchemy import SQLAlchemySchema
from app.extensions import ma
from marshmallow.validate import Length
from model.comment import Comment
from db import db


class CommentSchema(SQLAlchemySchema):
  class Meta:
    model = Comment
    load_instance = True
    sqla_session = db.session
  
  id = ma.UUID(dump_only=True)
  message = ma.String(validate=Length(min=3, max=255), required=True, allow_none=False)
  task_id = ma.UUID(required=True, allow_none=False)
  user_id = ma.UUID(required=True, allow_none=False)
  
  created_at = ma.DateTime(dump_only=True)
  updated_at = ma.DateTime(dump_only=True)
  
  task = ma.Nested('TaskSchema', dump_only=True)
  user = ma.Nested('UserSchema', dump_only=True)
  
comment_schema = CommentSchema()
comment_update_schema = CommentSchema(partial=True)
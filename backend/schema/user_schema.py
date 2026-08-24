from app import ma
from model import User
from schema import task_schema
from db import db

class UserSchema(ma.Schema):
  class Meta:
    model = User
    load_instance = True
    sqla_session = db.session
    
  id = ma.Integer(dump_only=True)
  first_name = ma.String(required=True, validate=ma.validate.Length(min=3, error='First name must be at least 3 characters.'), error_messages='First name is required')
  last_name = ma.String(required=True, validate=ma.validate.Length(min=3, error='Last name must be at least 3 characters.'), error_messages='Last name is required')
  email = ma.Email(required=True, validate=ma.validate.Regexp(r"^\S+@\S+\.\S+$", error="Invalid email format"), error_messages='Email is required')
  password = ma.String(required=True, validate=[ma.validate.Length(min=8, error='Password must be at least 8 characters.'), ma.validate.Regexp(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$", error='Password must contain: 8+ characters, uppercase, lowercase, number, and special character (!@#$%^&* etc.)')], load_only=True, error_messages='Password is required')
  created_at = ma.Datetime(dump_only=True)
  updated_at = ma.Datetime(dump_only=True)
  
  tasks = ma.Nested(task_schema, many=True, dump_only=True)
  
  
user_schema = UserSchema()
user_update_schema = UserSchema(partial=True)
from datetime import datetime, timezone
from schema import user_schema, user_update_schema
from utils.user_helper import email_exists, hash_password
from model.user import User, AccountStatus
from db import db
from marshmallow import ValidationError
from .workspace_service import create_workspace

class UserServiceError(Exception):
  status_code = 400

class Unauthorized(UserServiceError):
  status_code = 403

class EmailTaken(UserServiceError):
  status_code = 409

class NotFound(UserServiceError):
  status_code = 404

def create_user(data):
  first_name = (data.get('first_name') or '').strip()
  last_name = (data.get('last_name') or '').strip()
  email = (data.get('email') or '').lower().strip()
  password = (data.get('password') or '')
  if not all([first_name, last_name, email, password]):
    raise UserServiceError('All fields are required (first_name, last_name, email, and password)')

  errors = user_schema.validate({"first_name": first_name, "last_name": last_name, "email": email, "password": password})
  if errors:
    raise ValidationError(errors)

  if email_exists(email):
    raise EmailTaken('Email already exists')

  hashed_password = hash_password(password)
  # create user
  user = User(
    first_name=first_name,
    last_name=last_name,
    email=email,
    password_hash=hashed_password,
    account_status=AccountStatus.ACTIVE,
  )
  db.session.add(user)
  db.session.flush()

  # create default workspace
  workspace = create_workspace(user, {'name': f"{first_name}'s Workspace"}, commit=False)

  db.session.commit()

  return user, workspace

def get_me(current_user):
  if not current_user or not current_user.id:
    raise Unauthorized('User not authorized')

  user = db.session.get(User, current_user.id)
  if not user:
    raise NotFound('Profile not found')
  if not current_user or (current_user.id != user.id):
    raise Unauthorized('Not allowed to see users')
  return user

def update_me(id, data, current_user):
  user = db.session.get(User, id)
  if not user:
    raise NotFound('User not found')

  if not current_user or (current_user.id != user.id):
    raise Unauthorized('Only authorized user can edit this user')

  if 'email' in data:
    if data['email'] != user.email and email_exists(data['email']):
      raise EmailTaken('Email exists already')

  errors = user_update_schema.validate(data)
  if errors:
    raise ValidationError(errors)

  if 'first_name' in data:
    user.first_name = data['first_name'].strip()
  if 'last_name' in data:
    user.last_name = data['last_name'].strip()
  if 'email' in data:
    user.email = data['email'].lower().strip()
  if 'password' in data:
    user.password_hash = hash_password(data['password'])

  db.session.commit()

  return user

def delete_me(id, current_user):
  user = db.session.get(User, id)
  if not user:
    raise NotFound('User not found')

  if not current_user or (current_user.id != user.id):
    raise Unauthorized('Only authorized user can delete this user')

  user.account_status = AccountStatus.DELETED
  user.deleted_at = datetime.now(timezone.utc)

  db.session.commit()
  return user

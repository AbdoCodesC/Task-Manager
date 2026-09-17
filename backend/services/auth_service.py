from db import db
from model.user import User, AccountStatus
from flask_jwt_extended import get_jwt

class AuthServiceError(Exception):
  status_code = 400
  
class InvalidCredentials(AuthServiceError):
  status_code = 401
  
class Unauthorized(AuthServiceError):
  status_code = 403
  
def authenticate_user(data):
  email = (data.get('email') or '').lower().strip()
  password = data.get('password') or ''
  if not all([email, password]):
    raise AuthServiceError('Email and password are required')
  user = db.session.scalar(db.select(User).where(User.email == email))
  invalid_cred = not user or not user.check_password(password) or user.account_status != AccountStatus.ACTIVE
  if invalid_cred:
    raise InvalidCredentials('Invalid email or password')
  
  return user

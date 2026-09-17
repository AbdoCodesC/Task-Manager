from model.user import UserRole, User, AccountStatus
from db import db
from datetime import datetime, timezone

class AdminServiceError(Exception):
  status_code = 400
  
class NotFound(AdminServiceError):
  status_code = 404
  
class Unauthorized(AdminServiceError):
  status_code = 403

def require_platform_admin(user):
  if not user or user.role != UserRole.ADMIN:
    raise Unauthorized("Platform admin access required")

def get_admin_length():
  return db.session.scalars(db.select(User).where(User.role == UserRole.ADMIN)).all()

# admin - only
def get_user(admin_user, user_id):
  require_platform_admin(admin_user)
  user = db.session.get(User, user_id)
  if not user:
    raise NotFound('User not found')
  return user

def get_users(admin_user):
  require_platform_admin(admin_user)
  
  return db.session.scalars(db.select(User).order_by(User.created_at.desc())).all()

def suspend_user(admin_user, user_id):
  if not user_id:
    raise AdminServiceError('Invalid user id')
  
  require_platform_admin(admin_user)
  
  user = db.session.get(User, user_id)
  if not user:
    raise NotFound("User not found")
  if user.id == admin_user.id:
    raise AdminServiceError("You cannot suspend your own admin account")
  if user.role == UserRole.ADMIN:
    raise AdminServiceError("Cannot suspend another platform admin")
  
  user.account_status = AccountStatus.SUSPENDED
  user.token_version += 1
  
  db.session.commit()
  
  return user
  
def delete_user(admin_user, user_id):
  if not user_id:
    raise AdminServiceError('Invalid user id')
  require_platform_admin(admin_user)
  user = db.session.get(User, user_id)
  if not user:
    raise NotFound("User not found")
  if user.id == admin_user.id:
    raise AdminServiceError("You cannot delete your own admin account")
  if user.role == UserRole.ADMIN:
    raise AdminServiceError("Cannot delete another platform admin")
  
  admin_length = get_admin_length()
  if len(admin_length) <= 1:
    raise AdminServiceError("Unable to delete account, you are the last admin")
  
  user.account_status = AccountStatus.DELETED
  user.deleted_at = datetime.now(timezone.utc)
  user.token_version += 1
  
  db.session.commit()
  return user
  
  
def restore_user(admin_user, user_id):
  if not user_id:
    raise AdminServiceError('Invalid user id')
  require_platform_admin(admin_user)
  user = db.session.get(User, user_id)
  if not user:
    raise NotFound("User not found")
  
  user.account_status = AccountStatus.ACTIVE
  user.deleted_at = None
  user.token_version += 1
  
  db.session.commit()
  return user
  
def update_user(admin_user, user_id, data):
  if not user_id:
    raise AdminServiceError('Invalid user id')
  require_platform_admin(admin_user)
  if not data or 'role' not in data:
    raise AdminServiceError('Role is required')

  user = db.session.get(User, user_id)
  if not user:
    raise NotFound("User not found")
  if user.id == admin_user.id:
    raise AdminServiceError("You cannot update your own admin account")
  if user.role == UserRole.ADMIN:
    raise AdminServiceError("Cannot update another platform admin")

  try:
    user.role = UserRole(data['role'])
  except (KeyError, TypeError, ValueError):
    raise AdminServiceError("Role must be 'user' or 'admin'")
  
  db.session.commit()
  return user
  

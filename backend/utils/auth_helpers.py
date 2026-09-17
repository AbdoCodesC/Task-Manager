from flask_jwt_extended import get_jwt_identity
from model import User
from model.user import AccountStatus
from db import db

def get_current_user():
  try:
    user_id = get_jwt_identity()
    user = db.session.execute(db.select(User).where(User.id == user_id)).scalar_one_or_none()
    if not user or user.account_status != AccountStatus.ACTIVE:
      return None
    return user
  except (ValueError, TypeError):
    return None

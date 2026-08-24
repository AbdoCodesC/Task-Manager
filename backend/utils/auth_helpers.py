from flask_jwt_extended import get_jwt_identity
from model import User
from db import db

def get_current_user():
  try:
    user_id = get_jwt_identity()
    user = db.session.execute(db.select(User).where(User.id == user_id)).scalar_one_or_none()
    return user
  except (ValueError, TypeError):
    return None
  
def get_current_user_id():
  try:
    user_id = get_jwt_identity()
    return int(user_id) if user_id else None
  except (ValueError, TypeError):
    return None
    
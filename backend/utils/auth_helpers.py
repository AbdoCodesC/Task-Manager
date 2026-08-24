from flask_jwt_extended import get_jwt_identity
from model import User

def get_current_user():
  try:
    user_id = get_jwt_identity()
    return User.query.get(int(user_id)) if user_id else None
  except (ValueError, TypeError):
    return None
  
def get_current_user_id():
  try:
    user_id = get_jwt_identity()
    return int(user_id) if user_id else None
  except (ValueError, TypeError):
    return None
    
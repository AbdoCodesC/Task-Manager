from db import db
from model import User
from app.extensions import bcrypt
      
def email_exists(email):
  return db.session.execute(db.select(User).where(User.email == email)).scalar_one_or_none()

def hash_password(password):
  return bcrypt.generate_password_hash(password, 10).decode('utf-8')

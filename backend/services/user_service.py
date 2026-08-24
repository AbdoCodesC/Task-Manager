from schema import user_schema
from utils import email_exists, hash_password
from model import User

def create_user_logic(data):
  if not data:
    return None, {'message': 'No data provided'}, 400
  first_name = data.get('first_name').strip()
  last_name = data.get('last_name').strip()
  email = data.get('email').lower().strip()
  password = data.get('password').strip()
  if not all(first_name, last_name, email, password):
    return None, {'message': 'All fields are required'}, 400
  error = user_schema.validate({"first_name": first_name, "last_name": last_name, "email": email, "password": password})
  if error:
    return None, {'error': error}, 400 
  
  if email_exists(email):
    return None, {"message": "Email already exists."}, 400 #TODO: FIX THIS

  hashed_password = hash_password(password)
  
  user = User(first_name=first_name, last_name=last_name, email=email, password=hashed_password)
  
  return user, None, 201

def get_user_by_email_logic(email):
  if not email:
    return None, {'message': 'Email is required'}, 400
  user = email_exists(email)
  if not user:
    return None, {'message': 'User not found'}, 404
  
  return user, None, 200
  
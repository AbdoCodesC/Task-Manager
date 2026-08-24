from flask import Blueprint, jsonify, request
from services.user_service import create_user_logic, get_user_by_email_logic
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, unset_jwt_cookies, set_access_cookies, unset_access_cookies, unset_refresh_cookies, get_jwt_identity
from db import db
from app.app import log

auth_bp = Blueprint('auth', __name__)

# SignUp
@auth_bp.route('/signup', methods=['POST'])
def signup():
  data = request.get_json()
  user, error, status = create_user_logic(data)
  if error:
    return jsonify(error), status
  
  try:
    db.session.add(user)
    db.session.commit()
  except Exception as e:
    log.error(f'Error creating user: {str(e)}')
    return jsonify({'message': 'Signup failed'}), 500
  
  # login_user(user)
  access_token = create_access_token(identity=str(user.id))
  refresh_token = create_refresh_token(identity=str(user.id))
  response = jsonify({'message':'User signed up successfully', 'access_token': access_token, 'refresh_token': refresh_token, 'user': user.to_dict()})
  set_access_cookies(response, access_token)
  # send welcome message to email! #TODO LATER ON!
  return response, 201

# Login -- use Session
@auth_bp.route('/login', methods=['POST'])
def login():
  data = request.get_json()
  if not data:
    return jsonify({'message': 'No data provided'}), 400
  email = data.get('email', '')
  password = data.get('password', '')
  if not email or not password:
    return jsonify({'message': 'Email and password are required'}), 400
  
  user, error, status = get_user_by_email_logic(email)
  if error:
    print('here!')
    return jsonify({'message': 'Invalid email or password'}), status

  if not user.check_password(password):
    return jsonify({'message': 'Invalid email or password'}), 401
  
  # both email and pass valid
  access_token = create_access_token(identity=str(user.id))
  refresh_token = create_refresh_token(identity=str(user.id))
  response = jsonify({'message':'User logged in successfully','access_token':access_token, 'refresh_token': refresh_token, 'user': user.to_dict()})
  set_access_cookies(response, access_token)
  return response, 200

@auth_bp.route('/refresh', methods=['POST'])
def refresh():
  current_user_id = get_jwt_identity()
  new_access_token = create_access_token(identity=current_user_id)
  response = jsonify({'access_token': new_access_token})
  set_access_cookies(response, new_access_token)
  return response, 200

# Logout
@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
  response = jsonify({'message': 'Logout successful'})
  unset_jwt_cookies(response)
  unset_access_cookies(response)
  unset_refresh_cookies(response)
  return response, 200 # redirect url to /

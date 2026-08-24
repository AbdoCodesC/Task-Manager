from flask import Blueprint, request, jsonify
from model import User
from db import db
from app import log, ma
from schema import user_update_schema
from project.Task_Manager.backend.utils.user_helper import email_exists, hash_password
from services.user_service import create_user_logic, get_user_by_email_logic
# from flask_login import login_required, current_user
from utils.auth_helpers import get_current_user_id, get_current_user
from flask_jwt_extended import jwt_required

user_bp = Blueprint('users', __name__)

# get all users - admin OR create user
@user_bp.route('/users')
@jwt_required()
def get_users():
  user = get_current_user()
  if not user.is_admin():
    return jsonify({'message':'Unauthorized'}), 403
  users = db.session.execute(db.select(User).order_by(User.id)).scalars().all()
  if not users:
    return jsonify({'users':[]}), 200
  return jsonify({'users': [user.to_dict() for user in users]}), 200

# get one user
@user_bp.route('/users/<int:id>')
@jwt_required()
def get_user(id):
  current_user = get_current_user()
  user = db.get_or_404(User, id)
  if not current_user or (current_user.id != user.id and not current_user.is_admin()):
    return jsonify({'message': 'Unauthorized'}), 403
  return jsonify({'user': user.to_dict()}), 200

'''
# get user by email
@user_bp.route('/users')
def get_user_by_email():
  data = request.get_json()
  if not data:
    return jsonify({'message': 'No data provided'}), 400
  email = data.get('email', '')
  user, error, status = get_user_by_email_logic(email)
  if error:
    return jsonify(error), status
  return jsonify({'user': user.to_dict()}), 200
'''

# create user - use for (signup) auth
@user_bp.route('/users', methods=['POST'])
def create_user():
  data = request.get_json()
  if not data:
    return jsonify({'message': 'No data provided'}), 400
  user, error, status = create_user_logic(data)
  if error:
    return jsonify({"error": error}), status 

  try:
    db.session.add(user)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    log.error(f'Error creating user {user.id}: {str(e)}')
    return jsonify({'message': 'An error occured while creating the user'}), 500
  
  return jsonify({'message': 'User created successfully.', 'user': user.to_dict()}), 201
    
# update user #TODO
@user_bp.route('/users/<int:id>', methods=['PATCH'])
@jwt_required()
def update_user(id):
  data = request.get_json()
  if not data:
    return jsonify({'message': 'No data provided'}), 400
  
  user = db.get_or_404(User, id)
  current_user = get_current_user()
  if not current_user or (current_user.id != user.id and not current_user.is_admin()):
    return jsonify({'message': 'Unauthorized'}), 403
    
  if 'email' in data:
    if data['email'] != user.email and email_exists(data['email']):
      return jsonify({'message':'Email already exists'}), 400
  
  try:
    user = user_update_schema.load(data, instance=user)
  except ma.ValidationError as error:
    log.error(f'Error updating user: {str(error.messages)}')
    return jsonify({'errors': str(error.messages)}), 400

  if 'password' in data:
    user.password = hash_password(data['password'])
  
  try:
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    log.error(f'Error updating user {user.id}: {str(e)}')
    return jsonify({'message': 'An error occured while updating the user'}), 500
  return jsonify({'message':'User updated successfully','user': user.to_dict()}), 200
  
# delete user
@user_bp.route('/users/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
  user = db.get_or_404(User, id)
  current_user = get_current_user()
  if not current_user or (current_user.id != user.id and not current_user.is_admin()):
    return jsonify({'message': 'Unauthorized'}), 403
    
  try:
    db.session.delete(user)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    log.error(f'Error deleting user {user.id}: {str(e)}')
    return jsonify({'message': 'An error occured while deleting the user'}), 500
    
  return '', 204
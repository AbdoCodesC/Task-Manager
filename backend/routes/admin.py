from db import db
from flask import Blueprint, jsonify, request
from utils.auth_helpers import get_current_user
from services.admin_service import get_user, get_users, delete_user, restore_user, suspend_user, update_user, AdminServiceError
from flask_jwt_extended import jwt_required
from app.extensions import limiter
import logging

log = logging.getLogger(__name__)

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@limiter.limit('60 per minute')
def get_users_route():
  admin_user = get_current_user()
  
  try:
    users = get_users(admin_user)
  except AdminServiceError as e:
    return jsonify({'error': str(e)}), e.status_code
  except Exception as e:
    log.error(f"Error getting users: {e}")
    return jsonify({'error': 'An error occured while fetching users'}), 500
 
  return jsonify({'users': [user.to_dict() for user in users]}), 200

@admin_bp.route('/users/<uuid:user_id>', methods=['GET'])
@jwt_required()
@limiter.limit('60 per minute')
def get_user_route(user_id):
  admin_user = get_current_user()
  
  try:
    user = get_user(admin_user, user_id)
  except AdminServiceError as e:
    return jsonify({'error': str(e)}), e.status_code
  except Exception as e:
    log.error(f"Error getting user: {e}")
    return jsonify({'error': 'An error occured while fetching user'}), 500
 
  return jsonify({'user': user.to_dict()}), 200
  

@admin_bp.route('/users/<uuid:user_id>/suspend', methods=['POST'])
@jwt_required()
@limiter.limit('30 per minute')
def suspend_user_route(user_id):
  admin_user = get_current_user()
    
  try:
    user = suspend_user(admin_user, user_id)
  except AdminServiceError as e:
    db.session.rollback()
    return jsonify({'error': str(e)}), e.status_code
  except Exception as e:
    db.session.rollback()
    log.error(f"Error suspending user: {e}")
    return jsonify({'error': 'An error occured while suspending user'}), 500
  
  return jsonify({'user': user.to_dict()}), 200

@admin_bp.route('/users/<uuid:user_id>/restore', methods=['POST'])
@jwt_required()
@limiter.limit('30 per minute')
def restore_user_route(user_id):
  admin_user = get_current_user()
      
  try:
    user = restore_user(admin_user, user_id)
  except AdminServiceError as e:
    db.session.rollback()
    return jsonify({'error': str(e)}), e.status_code
  except Exception as e:
    db.session.rollback()
    log.error(f"Error restoring user: {e}")
    return jsonify({'error': 'An error occured while restoring user'}), 500
  
  return jsonify({'user': user.to_dict()}), 200

@admin_bp.route('/users/<uuid:user_id>', methods=['DELETE'])
@jwt_required()
@limiter.limit('10 per hour')
def delete_user_route(user_id):
  admin_user = get_current_user()
        
  try:
    user = delete_user(admin_user, user_id)
  except AdminServiceError as e:
    db.session.rollback()
    return jsonify({'error': str(e)}), e.status_code
  except Exception as e:
    db.session.rollback()
    log.error(f"Error deleting user: {e}")
    return jsonify({'error': 'An error occured while deleting user'}), 500
  
  return jsonify({'user': user.to_dict()}), 200

# TODO - update role?
@admin_bp.route('/users/<uuid:user_id>', methods=['PATCH'])
@jwt_required()
@limiter.limit('60 per hour')
def update_user_route(user_id):
  admin_user = get_current_user()
  data = request.get_json(silent=True)
  if not data:
    return jsonify({'error': 'No data provided'}), 400
  
  try:
    user = update_user(admin_user, user_id, data)
  except AdminServiceError as e:
    db.session.rollback()
    return jsonify({'error': str(e)}), e.status_code
  except Exception as e:
    db.session.rollback()
    log.error(f"Error updating user: {e}")
    return jsonify({'error': 'An error occured while updating user'}), 500
  
  return jsonify({'user': user.to_dict()}), 200



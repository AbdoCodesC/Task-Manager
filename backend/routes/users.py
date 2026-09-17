import logging
from flask import Blueprint, request, jsonify
from db import db
from utils.auth_helpers import get_current_user
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from services.user_service import UserServiceError, update_me, delete_me, get_me
from app.extensions import limiter
from sqlalchemy.exc import IntegrityError

user_bp = Blueprint('user', __name__)
log = logging.getLogger(__name__)

@user_bp.route('/users/me')
@jwt_required()
@limiter.limit('60 per hour')
def get_profile_route():
  current_user = get_current_user()

  try:
    user = get_me(current_user)
  except UserServiceError as e:
    return jsonify({'error': str(e)}), e.status_code
  except Exception as e:
    log.error(f'Error listing profile for user {current_user.id}: {e}')
    return jsonify({'error': f'An error occured while listing user\'s profile'}), 500

  return jsonify({'user': user.to_dict()}), 200

@user_bp.route('/users/me', methods=['PATCH'])
@jwt_required()
@limiter.limit("30 per hour")
def update_profile_route():
  data = request.get_json(silent=True)
  if not data:
    return jsonify({'error': 'No data provided'}), 400

  current_user = get_current_user()

  try:
    user = update_me(current_user.id, data, current_user)
  except UserServiceError as e:
    db.session.rollback()
    return jsonify({'error': str(e)}), e.status_code
  except ValidationError as e:
    db.session.rollback()
    return jsonify({'errors': e.messages}), 400
  except IntegrityError as e:
    db.session.rollback()
    return jsonify({'errors': str(e)}), 400
  except Exception as e:
    db.session.rollback()
    log.error(f'Error updating user {current_user.id}: {e}')
    return jsonify({'error': f'An error occured while updating user'}), 500

  return jsonify({'message':'User updated successfully','user': user.to_dict()}), 200

@user_bp.route('/users/me', methods=['DELETE'])
@jwt_required()
@limiter.limit('1 per hour')
def delete_account_route():
  current_user = get_current_user()

  try:
    user = delete_me(current_user.id, current_user)
  except UserServiceError as e:
    db.session.rollback()
    return jsonify({'error': str(e)}), e.status_code
  except Exception as e:
    db.session.rollback()
    log.error(f'Error deleting user {current_user.id}: {str(e)}')
    return jsonify({'error': 'An error occured while deleting the user'}), 500

  return '', 204
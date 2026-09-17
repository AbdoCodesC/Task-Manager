
from db import db
import logging
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, unset_jwt_cookies, set_access_cookies, unset_access_cookies, unset_refresh_cookies, get_jwt_identity, set_refresh_cookies, get_jwt
from services.user_service import create_user, UserServiceError
from model.user import User, AccountStatus
from marshmallow import ValidationError
from services.auth_service import authenticate_user, AuthServiceError
from app.extensions import limiter
from sqlalchemy.exc import IntegrityError

log = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__)

# SignUp
@auth_bp.route('/signup', methods=['POST'])
@limiter.limit("3 per hour")
def signup():
  data = request.get_json(silent=True)
  if not data:
    return jsonify({'error': 'No data provided'}), 400

  try:
    user, workspace = create_user(data)
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
    log.error(f'Error creating user: {e}')
    return jsonify({'error': f'An error occured while creating user'}), 500

  access_token = create_access_token(identity=str(user.id), additional_claims={
    'token_version': user.token_version
  })
  refresh_token = create_refresh_token(identity=str(user.id), additional_claims={
    'token_version': user.token_version
  })

  response = jsonify({'message': 'User signed up successfully', 'user': user.to_dict(), 'workspace': workspace.to_dict()})
  set_access_cookies(response, access_token)
  set_refresh_cookies(response, refresh_token)
  # TODO: queue welcome email — don't send synchronously here
  return response, 201

# Login
@auth_bp.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
  data = request.get_json(silent=True)
  if not data:
    return jsonify({'error': 'No data provided'}), 400

  try:
    user = authenticate_user(data)
  except AuthServiceError as e:
    return jsonify({'error': str(e)}), e.status_code
  except Exception as e:
    log.error(f'Error logging in: {e}')
    return jsonify({'error': 'An error occured while logging in'}), 500

  # both email and pass valid
  access_token = create_access_token(identity=str(user.id), additional_claims={
    'token_version': user.token_version
  })
  refresh_token = create_refresh_token(identity=str(user.id), additional_claims={
    'token_version': user.token_version
  })
  response = jsonify({'message':'User logged in successfully', 'user': user.to_dict()})
  set_access_cookies(response, access_token)
  set_refresh_cookies(response, refresh_token)
  # TODO: queue welcome email — don't send synchronously here
  return response, 200

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
@limiter.limit("10 per minute")
def refresh():
  user_id = get_jwt_identity()
  old_refresh_jti = get_jwt()['jti']
  user = db.session.get(User, user_id)
  if not user or user.account_status != AccountStatus.ACTIVE:
    return jsonify({'error': 'Invalid refresh token'}), 401

  refresh_expires = current_app.config['JWT_REFRESH_TOKEN_EXPIRES']
  current_app.extensions['jwt_redis_blocklist'].set(
    old_refresh_jti,
    'revoked',
    ex=int(refresh_expires.total_seconds()),
  )

  access_token = create_access_token(identity=user_id, additional_claims={
    'token_version': user.token_version
  })
  refresh_token = create_refresh_token(identity=user_id, additional_claims={
    'token_version': user.token_version
  })

  response = jsonify({'message': 'Token refreshed'})
  set_access_cookies(response, access_token)
  set_refresh_cookies(response, refresh_token)

  return response, 200

@auth_bp.route('/verify_token')
@limiter.limit('10 per minute')
@jwt_required()
def token():
  return jsonify({'authenticated': True}), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
@limiter.limit('3 per minute')
def logout():
  jti = get_jwt()['jti']
  user_id = get_jwt_identity()
  current_app.extensions['jwt_redis_blocklist'].set(
    jti,
    'revoked',
    ex=current_app.config['JWT_ACCESS_TOKEN_EXPIRES'],
  )
  user = db.session.get(User, user_id)
  if user:
    user.token_version += 1
    db.session.commit()

  response = jsonify({'message': 'Logout successful'})
  unset_jwt_cookies(response)
  return response, 200 # redirect url to /

import logging
from db import db
from services.workspace_member_service import get_members, update_member, delete_member, WorkspaceMemberServiceError
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from utils.auth_helpers import get_current_user
from marshmallow import ValidationError

workspace_member_bp = Blueprint('workspace_member', __name__)
log = logging.getLogger(__name__)

'''
GET    /api/workspaces/<workspace_id>/members
PATCH  /api/workspaces/<workspace_id>/members/<member_id>
DELETE /api/workspaces/<workspace_id>/members/<member_id>
'''

@workspace_member_bp.route('/<uuid:workspace_id>/members')
@jwt_required()
def get_members_route(workspace_id):
  user = get_current_user()
  try:
    members = get_members(workspace_id, user)
  except WorkspaceMemberServiceError as e:
    return jsonify({'error': str(e)}), e.status_code
  except Exception as e:
    log.error(f'Error fetching members')
    return jsonify({'error': 'An error occured while fetching members'}), 500

  return jsonify({'members': [member.to_dict() for member in members]}), 200

@workspace_member_bp.route('/<uuid:workspace_id>/members/<uuid:member_id>', methods=['PATCH'])
@jwt_required()
def update_member_route(workspace_id, member_id):
  user = get_current_user()
  data = request.get_json(silent=True)
  try:
    member = update_member(workspace_id, member_id, user, data)
  except WorkspaceMemberServiceError as e:
    db.session.rollback()
    return jsonify({'error': str(e)}), e.status_code
  except ValidationError as e:
    return jsonify({'error': str(e)}), 400
  except Exception as e:
    db.session.rollback()
    log.error(f'Error updating member')
    return jsonify({'error': 'An error occured while updating member'}), 500

  return jsonify({'members': member.to_dict()}), 200

@workspace_member_bp.route('/<uuid:workspace_id>/members/<uuid:member_id>', methods=['DELETE'])
@jwt_required()
def delete_member_route(workspace_id, member_id):
  user = get_current_user()
  
  try:
    delete_member(workspace_id, member_id, user)
  except WorkspaceMemberServiceError as e:
    db.session.rollback()
    return jsonify({'error': str(e)}), e.status_code
  except Exception as e:
    db.session.rollback()
    log.error(f'Error deleting member')
    return jsonify({'error': 'An error occured while deleting member'}), 500

  return '', 204
import logging
from db import db
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from utils.auth_helpers import get_current_user
from services.workspace_service import get_workspaces, WorkspaceServiceError, get_workspace, create_workspace, delete_workspace, update_workspace
from marshmallow import ValidationError

workspace_bp = Blueprint('workspace', __name__)
log = logging.getLogger(__name__)

@workspace_bp.route('/workspaces')
@jwt_required()
def get_workspaces_route():
  user = get_current_user()
  
  try:
    workspaces = get_workspaces(user)
  except WorkspaceServiceError as e:
    return jsonify({'error': str(e)}), e.status_code
  except Exception as e:
    log.error(f'Error fetching workspaces for user {user.id}: {e}')
    return jsonify({'error': 'An error occured while fetching workspace'}), 500
  
  return jsonify({'workspaces': [workspace.to_dict() for workspace in workspaces]}), 200

@workspace_bp.route('/workspaces/<uuid:workspace_id>')
@jwt_required()
def get_workspace_route(workspace_id):
  user = get_current_user()
  
  try:
    workspace = get_workspace(workspace_id, user)  
  except WorkspaceServiceError as e:
    return jsonify({'error': str(e)}), e.status_code
  except Exception as e:
    log.error(f'Error fetching workspaces for user {user.id}: {e}')
    return jsonify({'error': 'An error occured while fetching workspace'}), 500
  
  return jsonify({'workspace': workspace.to_dict()}), 200

@workspace_bp.route('/workspaces', methods=['POST'])
@jwt_required()
def create_workspace_route():
  user = get_current_user()
  data = request.get_json(silent=True)
  
  try:
    workspace = create_workspace(user, data)
  except WorkspaceServiceError as e:
    db.session.rollback()
    return jsonify({'error': str(e)}), e.status_code
  except ValidationError as e:
    return jsonify({'error': str(e)}), 400
  except Exception as e:
    db.session.rollback()
    log.error(f'Error creating workspace {e}')
    return jsonify({'error': 'An error occured while creating workspace'}), 500
  
  return jsonify({'message': 'Workspace created successfully', 'workspace': workspace.to_dict()}), 201

@workspace_bp.route('/workspaces/<uuid:workspace_id>', methods=['PATCH'])
@jwt_required()
def update_workspace_route(workspace_id):
  user = get_current_user()
  data = request.get_json(silent=True)
  
  try:
    workspace = update_workspace(workspace_id, user, data)
  except WorkspaceServiceError as e:
    db.session.rollback()
    return jsonify({'error': str(e)}), e.status_code
  except ValidationError as e:
    return jsonify({'error': str(e)}), 400
  except Exception as e:
    db.session.rollback()
    log.error(f'Error updating workspace {workspace_id}: {e}')
    return jsonify({'error': 'An error occured while updating workspace'}), 500
  
  return jsonify({'message': 'Workspace updated successfully', 'workspace': workspace.to_dict()}), 200

@workspace_bp.route('/workspaces/<uuid:workspace_id>', methods=['DELETE'])
@jwt_required()
def delete_workspace_route(workspace_id):
  user = get_current_user()
  
  try:
    delete_workspace(workspace_id, user)
  except WorkspaceServiceError as e:
    db.session.rollback()
    return jsonify({'error': str(e)}), e.status_code
  except Exception as e:
    db.session.rollback()
    log.error(f'Error deleting workspace {workspace_id}: {e}')
    return jsonify({'error': 'An error occured while deleting workspace'}), 500
  
  return '', 204
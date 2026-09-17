import logging
from db import db
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from utils.auth_helpers import get_current_user
from services.project_service import get_projects, get_project, create_project, update_project, delete_project, ProjectServiceError
from marshmallow import ValidationError

project_bp = Blueprint('project', __name__)
log = logging.getLogger(__name__)

@project_bp.route('/<uuid:workspace_id>/projects')
@jwt_required()
def get_projects_route(workspace_id):
  user = get_current_user()
  
  try:
    projects = get_projects(workspace_id, user)
  except ProjectServiceError as e:
    return jsonify({'error': str(e)}), e.status_code
  except Exception as e:
    log.error(f'Error fetching projects for workspace {workspace_id} user {user.id}: {e}')
    return jsonify({'error': 'An error occured while fetching projects'}), 500
  
  return jsonify({'projects': [project.to_dict() for project in projects]}), 200

@project_bp.route('/<uuid:workspace_id>/projects/<uuid:project_id>')
@jwt_required()
def get_project_route(workspace_id, project_id):
  user = get_current_user()
  
  try:
    project = get_project(workspace_id, project_id, user)
  except ProjectServiceError as e:
    return jsonify({'error': str(e)}), e.status_code
  except Exception as e:
    log.error(f'Error fetching project {project_id} for workspace {workspace_id} user {user.id}: {e}')
    return jsonify({'error': 'An error occured while fetching projects'}), 500
  
  return jsonify({'project': project.to_dict()}), 200

@project_bp.route('/<uuid:workspace_id>/projects', methods=['POST'])
@jwt_required()
def create_project_route(workspace_id):
  user = get_current_user()
  data = request.get_json(silent=True)
  
  try:
    project = create_project(workspace_id, user, data)
  except ProjectServiceError as e:
    db.session.rollback()
    return jsonify({'error': str(e)}), e.status_code
  except ValidationError as e:
    return jsonify({'error': str(e)}), 400
  except Exception as e:
    db.session.rollback()
    log.error(f'Error creating project for workspace {workspace_id} user {user.id}: {e}')
    return jsonify({'error': 'An error occured while creating project'}), 500
  
  return jsonify({'message': 'Project created successfully','project': project.to_dict()}), 201

@project_bp.route('/<uuid:workspace_id>/projects/<uuid:project_id>', methods=['PATCH'])
@jwt_required()
def update_project_route(workspace_id, project_id):
  user = get_current_user()
  data = request.get_json(silent=True)
  
  try:
    project = update_project(workspace_id, project_id, user, data)
  except ProjectServiceError as e:
    db.session.rollback()
    return jsonify({'error': str(e)}), e.status_code
  except ValidationError as e:
    return jsonify({'error': str(e)}), 400
  except Exception as e:
    db.session.rollback()
    log.error(f'Error updating project {project_id} for workspace {workspace_id} user {user.id}: {e}')
    return jsonify({'error': 'An error occured while updating project'}), 500
  
  return jsonify({'project': project.to_dict()}), 200

@project_bp.route('/<uuid:workspace_id>/projects/<uuid:project_id>', methods=['DELETE'])
@jwt_required()
def delete_project_route(workspace_id, project_id):
  user = get_current_user()
  
  try:
    delete_project(workspace_id, project_id, user)
  except ProjectServiceError as e:
    db.session.rollback()
    return jsonify({'error': str(e)}), e.status_code
  except Exception as e:
    db.session.rollback()
    log.error(f'Error deleting project {project_id} for workspace {workspace_id} user {user.id}: {e}')
    return jsonify({'error': 'An error occured while deleting project'}), 500
  
  return '', 204
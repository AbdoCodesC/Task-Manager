import logging
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from db import db
from utils.auth_helpers import get_current_user
from services.task_service import delete_task, get_tasks, get_task, update_task, create_task, TaskServiceError
from marshmallow import ValidationError

task_bp = Blueprint('task', __name__)
log = logging.getLogger(__name__)

# /workspaces       /<id>/projects/<id>/task
@task_bp.route('/<uuid:workspace_id>/projects/<uuid:project_id>/tasks', methods=["GET"])
@jwt_required()
def get_tasks_route(workspace_id, project_id):
  user = get_current_user()

  try:
    tasks = get_tasks(workspace_id, project_id, user)
  except TaskServiceError as e:
    return jsonify({'error': str(e)}), e.status_code
  except Exception as e:
    log.error(f'Error fetching tasks for workspace {workspace_id} project {project_id}: {e}')
    return jsonify({'error': 'An error occured while fetching tasks'}), 500

  return jsonify({'tasks': [task.to_dict() for task in tasks]}), 200


@task_bp.route('/<uuid:workspace_id>/projects/<uuid:project_id>/tasks/<uuid:task_id>', methods=["GET"])
@jwt_required()
def get_task_route(task_id, workspace_id, project_id):
  user = get_current_user()

  try:
    task = get_task(task_id, workspace_id, project_id, user)
  except TaskServiceError as e:
    return jsonify({'error': str(e)}), e.status_code
  except Exception as e:
    log.error(f'Error fetching task {task_id} for workspace {workspace_id} project {project_id}: {e}')
    return jsonify({'error': 'An error occured while fetching task'}), 500

  return jsonify({'task': task.to_dict()}), 200

@task_bp.route('/<uuid:workspace_id>/projects/<uuid:project_id>/tasks', methods=['POST'])
@jwt_required()
def create_task_route(workspace_id, project_id):
  user = get_current_user()
  data = request.get_json(silent=True)

  try:
    task = create_task(workspace_id, project_id, user, data)
  except TaskServiceError as e:
    db.session.rollback()
    return jsonify({'error': str(e)}), e.status_code
  except ValidationError as e:
    return jsonify({'error': str(e)}), 400
  except Exception as e:
    db.session.rollback()
    log.error(f'Error creating task for workspace {workspace_id} project {project_id}: {e}')
    return jsonify({'error': 'An error occured while creating task'}), 500

  return jsonify({'task': task.to_dict()}), 201

@task_bp.route('/<uuid:workspace_id>/projects/<uuid:project_id>/tasks/<uuid:task_id>', methods=['PATCH'])
@jwt_required()
def update_task_route(task_id, workspace_id, project_id):
  user = get_current_user()
  data = request.get_json(silent=True)

  try:
    task = update_task(task_id, workspace_id, project_id, user, data)
  except TaskServiceError as e:
    db.session.rollback()
    return jsonify({'error': str(e)}), e.status_code
  except ValidationError as e:
    return jsonify({'error': str(e)}), 400
  except Exception as e:
    db.session.rollback()
    log.error(f'Error updating task for workspace {workspace_id} project {project_id}: {e}')
    return jsonify({'error': 'An error occured while updating task'}), 500

  return jsonify({'task': task.to_dict()}), 200

@task_bp.route('/<uuid:workspace_id>/projects/<uuid:project_id>/tasks/<uuid:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task_route(task_id, workspace_id, project_id):
  user = get_current_user()

  try:
    delete_task(task_id, workspace_id, project_id, user)
  except TaskServiceError as e:
    db.session.rollback()
    return jsonify({'error': str(e)}), e.status_code
  except Exception as e:
    db.session.rollback()
    log.error(f'Error deleting task {task_id} for workspace {workspace_id} project {project_id}: {e}')
    return jsonify({'error': 'An error occured while deleting task'}), 500

  return '', 204


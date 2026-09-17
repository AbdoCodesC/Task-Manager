import logging
from db import db
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from utils.auth_helpers import get_current_user
from services.time_block_service import get_time_blocks, create_time_block, update_time_block, delete_time_block, TimeBlockServiceError
from marshmallow import ValidationError

time_block_bp = Blueprint('time_block', __name__)
log = logging.getLogger(__name__)
"""
  GET    /api/tasks/<task_id>/time-blocks
  POST   /api/tasks/<task_id>/time-blocks
  PATCH  /api/time-blocks/<time_block_id>
  DELETE /api/time-blocks/<time_block_id>
"""
@time_block_bp.route('/tasks/<uuid:task_id>/time_blocks')
@jwt_required()
def get_time_blocks_route(task_id):
  user = get_current_user()
    
  try:
    time_blocks = get_time_blocks(task_id, user)
  except TimeBlockServiceError as e:
    return jsonify({'error': str(e)}), e.status_code
  except Exception as e:
    log.error(f'Error occured while fetching time blocks: {e}')
    return jsonify({'error': 'An error occured while fetching time blocks'}), 500
  
  return jsonify({'time_blocks': [time_block.to_dict() for time_block in time_blocks]}), 200

@time_block_bp.route('/tasks/<uuid:task_id>/time_blocks', methods=['POST'])
@jwt_required()
def create_time_block_route(task_id):
  user = get_current_user()
  data = request.get_json(silent=True)
  
  try:
    time_block = create_time_block(task_id, user, data)
  except TimeBlockServiceError as e:
    db.session.rollback()
    return jsonify({'error': str(e)}), e.status_code
  except ValidationError as e:
    return jsonify({'error': str(e)}), 400
  except Exception as e:
    db.session.rollback()
    log.error(f'Error occured while creating time block: {e}')
    return jsonify({'error': 'An error occured while creating time block'}), 500
  
  return jsonify({'time_block': time_block.to_dict()}), 201

@time_block_bp.route('/tasks/<uuid:task_id>/time_blocks/<uuid:time_block_id>', methods=['PATCH'])
@jwt_required()
def update_time_block_route(task_id, time_block_id):
  user = get_current_user()
  data = request.get_json(silent=True)
  
  try:
    time_block = update_time_block(time_block_id, task_id, user, data)
  except TimeBlockServiceError as e:
    db.session.rollback()
    return jsonify({'error': str(e)}), e.status_code
  except ValidationError as e:
    return jsonify({'error': str(e)}), 400
  except Exception as e:
    db.session.rollback()
    log.error(f'Error occured while updating time block: {e}')
    return jsonify({'error': 'An error occured while updating time block'}), 500
  
  return jsonify({'time_block': time_block.to_dict()}), 200

@time_block_bp.route('/tasks/<uuid:task_id>/time_blocks/<uuid:time_block_id>', methods=['DELETE'])
@jwt_required()
def delete_time_block_route(task_id, time_block_id):
  user = get_current_user()
  
  try:
    delete_time_block(time_block_id, task_id, user)
  except TimeBlockServiceError as e:
    db.session.rollback()
    return jsonify({'error': str(e)}), e.status_code
  except Exception as e:
    db.session.rollback()
    log.error(f'Error occured while deleting time block: {e}')
    return jsonify({'error': 'An error occured while deleting time block'}), 500
  
  return '', 204
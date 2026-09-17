import logging
from db import db
from flask_jwt_extended import jwt_required
from utils.auth_helpers import get_current_user
from flask import Blueprint, jsonify, request
from services.comment_service import get_comments, create_comment, update_comment, delete_comment, CommentServiceError
from marshmallow import ValidationError

comment_bp = Blueprint('comment', __name__)
log = logging.getLogger(__name__)

@comment_bp.route("/tasks/<uuid:task_id>/comments", methods=["GET"])
@jwt_required()
def get_comments_route(task_id):
  user = get_current_user()
  
  try:
    comments = get_comments(task_id, user)
  except CommentServiceError as e:
    return jsonify({'error': str(e)}), e.status_code
  except Exception as e:
    log.error(f'Error occured while fetching comments: {e}')
    return jsonify({'error': 'An error occured while fetching comments'}), 500
  
  return jsonify({'comments': [comment.to_dict() for comment in comments]}), 200

@comment_bp.route("/tasks/<uuid:task_id>/comments", methods=["POST"])
@jwt_required()
def create_comment_route(task_id):
  user = get_current_user()
  data = request.get_json(silent=True)
  
  try:
    comment = create_comment(task_id, user, data)
  except CommentServiceError as e:
    db.session.rollback()
    return jsonify({'error': str(e)}), e.status_code
  except ValidationError as e:
    return jsonify({'error': str(e)}), 400
  except Exception as e:
    db.session.rollback()
    log.error(f'Error occured while creating comment: {e}')
    return jsonify({'error': 'An error occured while creating comments'}), 500
  
  return jsonify({'comment': comment.to_dict()}), 201

@comment_bp.route("/comments/<uuid:comment_id>", methods=["PATCH"])
@jwt_required()
def update_comment_route(comment_id):
  user = get_current_user()
  data = request.get_json(silent=True)
  
  try:
    comment = update_comment(comment_id, user, data)
  except CommentServiceError as e:
    db.session.rollback()
    return jsonify({'error': str(e)}), e.status_code
  except ValidationError as e:
    return jsonify({'error': str(e)}), 400
  except Exception as e:
    db.session.rollback()
    log.error(f'Error occured while updating comment: {e}')
    return jsonify({'error': 'An error occured while updating comment'}), 500
  
  return jsonify({'comment': comment.to_dict()}), 200

@comment_bp.route("/comments/<uuid:comment_id>", methods=["DELETE"])
@jwt_required()
def delete_comment_route(comment_id):
  user = get_current_user()
  
  try:
    delete_comment(comment_id, user)
  except CommentServiceError as e:
    db.session.rollback()
    return jsonify({'error': str(e)}), e.status_code
  except Exception as e:
    db.session.rollback()
    log.error(f'Error occured while deleting comment: {e}')
    return jsonify({'error': 'An error occured while deleting comment'}), 500
  
  return '', 204
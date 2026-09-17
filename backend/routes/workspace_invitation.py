import logging
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from utils.auth_helpers import get_current_user
from services.workspace_invitation_service import get_workspace_invitations, create_workspace_invitation, delete_workspace_invitation, WorkspaceInvitationServiceError, accept_invitation, decline_invitation
from db import db
from marshmallow import ValidationError

workspace_invitation_bp = Blueprint('workspace_invitation', __name__)
log = logging.getLogger(__name__)

@workspace_invitation_bp.route('/<uuid:workspace_id>/invitations')
@jwt_required()
def get_workspace_invitations_route(workspace_id):
  user = get_current_user()
  
  try: 
    invitations = get_workspace_invitations(workspace_id, user)
  except WorkspaceInvitationServiceError as e:
    return jsonify({'error': str(e)}), e.status_code
  except Exception as e:
    log.error(f'Error occured fetching workspace invitations: {e}')
    return jsonify({'error': 'An error occured while fetching workspace invitations'}), 500
  
  return jsonify({'invitations': [invitation.to_dict() for invitation in invitations]}), 200

@workspace_invitation_bp.route('/<uuid:workspace_id>/invitations', methods=['POST'])
@jwt_required()
def create_workspace_invitations_route(workspace_id):
  user = get_current_user()
  data = request.get_json(silent=True)
  
  try: 
    invitation = create_workspace_invitation(workspace_id, user, data)
  except WorkspaceInvitationServiceError as e:
    db.session.rollback()
    return jsonify({'error': str(e)}), e.status_code
  except ValidationError as e:
      return jsonify({'error': str(e)}), 400
  except Exception as e:
    db.session.rollback()
    log.error(f'Error occured creating workspace invitation: {e}')
    return jsonify({'error': 'An error occured while creating workspace invitation'}), 500
  
  return jsonify({'invitation': invitation.to_dict() }), 201


@workspace_invitation_bp.route('/<uuid:workspace_id>/invitations/<uuid:invitation_id>', methods=['DELETE'])
@jwt_required()
def delete_workspace_invitation_route(workspace_id, invitation_id):
  user = get_current_user()
  
  try:
    delete_workspace_invitation(workspace_id, invitation_id, user)
  except WorkspaceInvitationServiceError as e:
    db.session.rollback()
    return jsonify({'error': str(e)}), e.status_code
  except Exception as e:
    db.session.rollback()
    log.error(f'Error occured deleting workspace invitation: {e}')
    return jsonify({'error': 'An error occured while deleting workspace invitation'}), 500
  
  return '', 204

@workspace_invitation_bp.route('/invitations/<uuid:token>/accept', methods=['POST'])
@jwt_required()
def accept_invitation_route(token):
  user = get_current_user()
  
  try:
    membership = accept_invitation(token, user)
  except WorkspaceInvitationServiceError as e:
    db.session.rollback()
    return jsonify({'error': str(e)}), e.status_code
  except Exception as e:
    db.session.rollback()
    log.error(f'Error occured while accepting invitation: {e}')
    return jsonify({'error': 'An error occured while accepting invitation'}), 500
  
  return jsonify({'message': f'Welcome to workspace', 'workspace': membership.to_dict()}), 200

@workspace_invitation_bp.route('/invitations/<uuid:token>/decline', methods=['POST'])
@jwt_required()
def decline_invitation_route(token):
  user = get_current_user()
  
  try:
    invitation = decline_invitation(token, user)
  except WorkspaceInvitationServiceError as e:
    db.session.rollback()
    return jsonify({'error': str(e)}), e.status_code
  except Exception as e:
    db.session.rollback()
    log.error(f'Error occured while declining invitation: {e}')
    return jsonify({'error': 'An error occured while declining invitation'}), 500
  
  return jsonify({'message': f'Declined invitation to {invitation.workspace.name}'}), 200
from db import db
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from utils.auth_helpers import get_current_user
from services.analytic_service import get_analytics, AnalyticServiceError
import logging
from app.extensions import limiter

log = logging.getLogger(__name__)
analytic_bp = Blueprint('analytic', __name__)

@analytic_bp.route('/<uuid:workspace_id>/analytics')
@jwt_required()
@limiter.limit('60 per hour')
def get_analytics_route(workspace_id):
  user = get_current_user()
 
  try: 
    analytics = get_analytics(user, workspace_id)
  except AnalyticServiceError as e:
    return jsonify({'error': str(e)}), e.status_code
  except Exception as e:
    log.error(f"Error fetching analytics: {e}")
    return jsonify({'error': 'An error occured while fetching analytics'}), 500

  return jsonify(analytics), 200
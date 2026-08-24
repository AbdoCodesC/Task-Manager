from flask import Blueprint, jsonify

health_bp = Blueprint('health_check', __name__)

@health_bp.route('/')
def check():
  return jsonify({'message': 'Server is up'}), 200
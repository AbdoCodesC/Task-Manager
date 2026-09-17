# source: https://flask.palletsprojects.com/en/stable/patterns/sqlalchemy/
import os
from flask import Flask, jsonify
import logging as log
from db import db
from routes import user_bp, task_bp, auth_bp, health_bp, workspace_bp, project_bp, workspace_member_bp, workspace_invitation_bp, time_block_bp, comment_bp, admin_bp, analytic_bp
from dotenv import load_dotenv
from app.extensions import bcrypt, jwt_manager, migrate, ma, limiter
from flask_cors import CORS
import redis
from app.config import DevelopmentConfig
from model import User

load_dotenv()

def create_app():
  app = Flask(__name__)

  # Load config
  app.config.from_object(DevelopmentConfig)

  # log
  os.makedirs('./log', exist_ok=True)
  log.basicConfig(level=log.INFO, filename="./log/app.log", format="%(asctime)s - %(levelname)s - %(message)s")

  # load .env
  required_env = ['REDIS_HOST', 'REDIS_PORT', 'REDIS_DB', 'REDIS_DB', 'JWT_SECRET', 'DATABASE_URI', 'DEV_HOST']
  missing = [var for var in required_env if not os.getenv(var)]
  if missing:
    raise RuntimeError(f"Missing environment variables: {', '.join(missing)}")

  # Redis
  jwt_redis_blocklist = redis.StrictRedis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'], db=app.config['REDIS_DB'], decode_responses=True)
  app.extensions['jwt_redis_blocklist'] = jwt_redis_blocklist
  @jwt_manager.token_in_blocklist_loader
  def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload['jti']
    token_in_redis = jwt_redis_blocklist.get(jti)
    if token_in_redis is not None:
      return True

    user = db.session.get(User, jwt_payload.get('sub'))
    token_version = jwt_payload.get('token_version')
    return not user or token_version != user.token_version

  @app.errorhandler(429)
  def ratelimit_handler(error):
    response = jsonify({'error': 'rate_limit_exceeded', 'message': 'Too many requests. Please try again later.'})
    response.status_code = 429
    return response

  # Extensions
  limiter.init_app(app)
  jwt_manager.init_app(app)
  bcrypt.init_app(app)
  db.init_app(app)
  migrate.init_app(app, db)
  ma.init_app(app) # Order matters: Initialize SQLAlchemy before Marshmallow

  # Rate limits
  limiter.limit('200 per hour')(workspace_bp)
  limiter.limit('200 per hour')(workspace_member_bp)
  limiter.limit('20 per hour')(workspace_invitation_bp)
  limiter.limit('200 per hour')(project_bp)
  limiter.limit('200 per hour')(task_bp)
  limiter.limit('200 per hour')(comment_bp)
  limiter.limit('200 per hour')(time_block_bp)

  # Blueprints
  app.register_blueprint(health_bp, url_prefix='/api/health')
  app.register_blueprint(analytic_bp, url_prefix='/api/workspaces')
  app.register_blueprint(user_bp, url_prefix='/api')
  app.register_blueprint(auth_bp, url_prefix='/api/auth')
  app.register_blueprint(workspace_bp, url_prefix='/api')
  app.register_blueprint(workspace_member_bp, url_prefix='/api/workspaces')
  app.register_blueprint(workspace_invitation_bp, url_prefix='/api/workspaces')
  app.register_blueprint(project_bp, url_prefix='/api/workspaces')
  app.register_blueprint(task_bp, url_prefix='/api/workspaces')
  app.register_blueprint(comment_bp, url_prefix='/api')
  app.register_blueprint(time_block_bp, url_prefix='/api')
  app.register_blueprint(admin_bp, url_prefix='/api/admin')

  # Cors
  CORS(app, origins=app.config['CORS_ORIGINS'], allow_headers=app.config['CORS_ALLOW_HEADERS'], supports_credentials=app.config['CORS_SUPPORTS_CREDENTIALS'])

  return app



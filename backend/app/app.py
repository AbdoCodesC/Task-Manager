# source: https://flask.palletsprojects.com/en/stable/patterns/sqlalchemy/
import os
from datetime import timedelta
from flask import Flask
import logging as log
from db import db
from routes import user_bp, task_bp, auth_bp, health_bp
from dotenv import load_dotenv
from app.extensions import bcrypt, jwt_manager, migrate, ma

load_dotenv()

os.makedirs('./log', exist_ok=True)
log.basicConfig(level=log.INFO, filename="./log/app.log", format="%(asctime)s - %(levelname)s - %(message)s")

def create_app():
  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task_manager.db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET", 'secret') 
  app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
  
  jwt_manager.init_app(app)
  bcrypt.init_app(app)

  db.init_app(app)
  migrate.init_app(app, db)
  # Order matters: Initialize SQLAlchemy before Marshmallow
  ma.init_app(app)
  
  app.register_blueprint(user_bp, url_prefix='/api/users')
  app.register_blueprint(task_bp, url_prefix='/api/tasks')
  app.register_blueprint(auth_bp, url_prefix='/api/auth')
  app.register_blueprint(health_bp, url_prefix='/api/health')
  
  with app.app_context():
    db.create_all()
  
  return app


  
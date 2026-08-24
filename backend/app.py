# source: https://flask.palletsprojects.com/en/stable/patterns/sqlalchemy/
from flask import Flask
import logging as log
from db import db
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from routes import user_bp, task_bp, auth_bp
import os
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
load_dotenv()

os.makedirs('./log', exist_ok=True)
log.basicConfig(level=log.INFO, filename="./log/app.log", format="%(asctime)s - %(levelname)s - %(message)s")

ma = Marshmallow()
bcrypt = Bcrypt()
migrate = Migrate()
jwt_manager = JWTManager()

def create_app():
  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task_manager.db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET", 'secret') 
  
  jwt_manager.init_app(app)
  bcrypt.init_app(app)

  db.init_app(app)
  migrate.init_app(app, db)
  # Order matters: Initialize SQLAlchemy before Marshmallow
  ma.init_app(app)
  
  app.register_blueprint(user_bp)
  app.register_blueprint(task_bp)
  app.register_blueprint(auth_bp)
  
  with app.app_context():
    db.create_all()
  
  return app


  
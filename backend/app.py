# source: https://flask.palletsprojects.com/en/stable/patterns/sqlalchemy/
from flask import Flask
import logging as log
log.basicConfig(level=log.INFO, filename="./log/app-py.log")
from db import db
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

def create_app():
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task_manager.db'

  db.init_db(app)
  
  with app.app_context():
    db.create_all()


  
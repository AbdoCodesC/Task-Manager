from flask_sqlalchemy import SQLAlchemy
from model.base import Base

db = SQLAlchemy(model_class=Base)
  
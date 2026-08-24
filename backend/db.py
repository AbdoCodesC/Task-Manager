from flask_sqlalchemy import SQLAlchemy
from model import Base

db = SQLAlchemy(model_class=Base)
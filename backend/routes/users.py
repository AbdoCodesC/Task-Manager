from backend.app import app
from flask import Blueprint, request, jsonify
from model import User
from db import db
from app import bcrypt
from utils import valid_data
user_bp = Blueprint('users', __name__)

# get all users - admin OR create user
@user_bp.route('/users', methods=["GET","POST"])
def get_users():
  if request.method == "POST":
    first_name, last_name, email, password = request.body
    if not valid_data(first_name, last_name, email, password):
      #TODO: FIX THIS 
      return jsonify({"message": "Data is not valid, make sure all data is valid"}) 
  users = db.session.execute(db.select(User).order_by(User.id)).scalars()
  return [user.to_dict() for user in users], 200

@user_bp.route('/users/<int:id>')
def get_user(id):
  user = db.get_or_404(id)
  return user.to_dict(), 200


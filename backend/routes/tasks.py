from model import Task
from flask import Blueprint, jsonify, request
from schema import task_schema, task_update_schema
from flask_jwt_extended import jwt_required
from db import db
from app import log, ma
from utils.auth_helpers import get_current_user_id

task_bp = Blueprint('tasks', __name__)

# get all tasks by user id
@task_bp.route('/tasks')
@jwt_required()
def get_tasks():
  # get current_user id
  user_id = get_current_user_id()
  if not user_id:
    return jsonify({'message': 'User not logged in, try to login first.'}), 401
  
  tasks = db.session.execute(db.select(Task).where(Task.user_id == user_id).order_by(Task.id)).scalars().all()
  if not tasks:
    return jsonify({'message':'No tasks found', 'tasks':[]}), 200
  
  return jsonify(task_schema.dump(tasks, many=True)), 200

# get certain task by user id
@task_bp.route('/tasks/<int:id>')
@jwt_required()
def get_task(id):
  user_id = get_current_user_id()
  if not user_id:
    return jsonify({'message': 'User not logged in, try to login first.'}), 401
  task = db.session.execute(db.select(Task).where(Task.user_id == user_id, Task.id == id)).scalar_one_or_none()
  if not task:
    return jsonify({'message': 'Task not found'}), 404
  return jsonify(task_schema.dump(task)), 200

# create task by user id
@task_bp.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
  data = request.get_json()
  if not data:
    return jsonify({'message': 'No data provided'}), 400
  user_id = get_current_user_id()
  if not user_id:
    return jsonify({'message': 'User not logged in, try to login first.'}), 401
  try:
    task = task_schema.load(data)
    task.user_id = user_id
  except ma.ValidationError as error:
    return jsonify({'error': str(error.messages)}), 400
  
  try:
    db.session.add(task)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    log.error(f'Error saving task for {task.user_id}: {str(e)}')
    return jsonify({'message':'An error occurred while creating the task'}), 500
  
  return jsonify({'message':'Task created successfully', 'task': task_schema.dump(task)}), 201

# update task by user id
@task_bp.route('/tasks/<int:id>', methods=['PATCH'])
@jwt_required()
def update_task(id):
  data = request.get_json()
  if not data:
    return jsonify({'message': 'No data provided'}), 400
  user_id = get_current_user_id()
  if not user_id:
    return jsonify({'message': 'User not logged in, try to login first.'}), 401

  task = db.session.execute(db.select(Task).where(Task.id == id, Task.user_id == user_id)).scalar_one_or_none() # get task
  if not task: 
    return jsonify({'message':'Task not found'}), 404
  
  try:
    task = task_update_schema.load(data, instance=task)
  except ma.ValidationError as error:
    log.error(f'Error updating task: {str(error)}')
    return jsonify({'error': str(error.messages)})
  
  try:
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    log.error(f'Error updating task for {task.user_id}: {str(e)}')
    return jsonify({'message':'An error occurred while updating the task'}), 500
  
  return jsonify({'message': 'Task updated successfully', 'task': task_schema.dump(task)}), 200

# delete task by user id
@task_bp.route('/tasks/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_task(id):
  task = db.session.execute(db.select(Task).where(Task.user_id == get_current_user_id(), Task.id == id)).scalar_one_or_none()
  if not task:
    return jsonify({'message': 'Task not found'}), 404
  try:
    db.session.delete(task)
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    log.error(f'Error deleting task {task.id}:{str(e)}')
    return jsonify({'message': 'Error deleting task'}), 500
  return '', 204
  

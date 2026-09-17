from db import db
from model import Project
from model.workspace_member import MemberRole
from schema import task_schema, task_update_schema
from marshmallow import ValidationError
from model.task import TaskPriority, TaskStatus, Task
from model.task_activity import TaskActivity, ActivityType
from datetime import datetime, timezone
from utils.workspace_member_helpers import get_workspace_membership

class TaskServiceError(Exception):
  status_code = 400
  
class Unauthorized(TaskServiceError):
  status_code = 403

class NotFound(TaskServiceError):
  status_code = 404
  

def get_project_in_workspace(workspace_id, project_id):
  project = db.session.scalar(db.select(Project).where(Project.id == project_id, Project.workspace_id == workspace_id))
  if not project:
    raise NotFound('Project not found in this workspace')
  return project


def get_tasks(workspace_id, project_id, user):
  get_workspace_membership(workspace_id, user)
  get_project_in_workspace(workspace_id, project_id)
  
  tasks = db.session.scalars(db.select(Task).join(Project).where(Task.project_id == project_id, Task.status != TaskStatus.ARCHIVED, Project.workspace_id == workspace_id).order_by(Task.created_at.desc())).all()
  
  return tasks

def get_task(task_id, workspace_id, project_id, user):
  get_workspace_membership(workspace_id, user)
  get_project_in_workspace(workspace_id, project_id)

  task = db.session.scalar(db.select(Task).join(Project).where(Task.project_id == project_id, Task.status != TaskStatus.ARCHIVED, Task.id == task_id, Project.workspace_id == workspace_id))
  if not task:
    raise NotFound('Task not found')
  
  return task

def create_task(workspace_id, project_id, user, data):
  membership = get_workspace_membership(workspace_id, user)
  if membership.role not in [MemberRole.ADMIN, MemberRole.OWNER]:
    raise Unauthorized('You do not have permission to create tasks')
  if not data:
    raise TaskServiceError('Data not provided')
  
  title = (data.get('title') or '').strip()
  description = (data.get('description') or '').strip()
  try:
    priority = TaskPriority(data.get('priority', TaskPriority.MEDIUM.value))
    status = TaskStatus(data.get('status', TaskStatus.TODO.value))
  except ValueError:
    raise TaskServiceError('Invalid task priority or status')
  errors = task_schema.validate({'title': title, 'description': description, 'priority': priority, 'status': status})
  if errors: 
    raise ValidationError(errors)
  
  get_project_in_workspace(workspace_id, project_id)
  
  task = Task(title=title, description=description, priority=priority, status=status, project_id=project_id)
  db.session.add(task)
  db.session.flush()
  
  activity = TaskActivity(task_id=task.id, user_id=user.id, activity_type=ActivityType.CREATED)
  db.session.add(activity)
  
  db.session.commit()
  
  return task

def update_task(task_id, workspace_id, project_id, user, data):
  membership = get_workspace_membership(workspace_id, user)
  if membership.role not in [MemberRole.ADMIN, MemberRole.OWNER]:
    raise Unauthorized('You do not have permission to update tasks')
  if not data:
    raise TaskServiceError('Data not provided')
  
  errors = task_update_schema.validate(data)
  if errors: 
    raise ValidationError(errors)
  
  task = get_task(task_id, workspace_id, project_id, user)
  activities = []
  
  if 'title' in data:
    new_title = data['title'].strip()
    if new_title != task.title:
      activities.append(TaskActivity(
        task_id=task.id,
        user_id=user.id,
        activity_type=ActivityType.UPDATED,
        field_name='title',
        old_value=task.title,
        new_value=new_title))
      task.title = new_title
  
  if 'description' in data:
    new_description = (data['description'].strip() if data['description'] is not None else None)
    if new_description != task.description:
      activities.append(TaskActivity(
        task_id=task.id,
        user_id=user.id,
        activity_type=ActivityType.UPDATED,
        field_name='description',
        old_value=task.description,
        new_value=new_description))
      task.description = new_description
    
  if 'priority' in data:
    new_priority = TaskPriority(data['priority'])
    if new_priority != task.priority:
      activities.append(TaskActivity(
        user_id=user.id,
        task_id=task.id,
        activity_type=ActivityType.PRIORITY_CHANGED,
        field_name='priority',
        old_value=task.priority.value,
        new_value=new_priority.value))
      task.priority = new_priority
  
  if 'status' in data:
    old_status = task.status
    new_status = TaskStatus(data['status'])
    if new_status != old_status:
      if new_status == TaskStatus.DONE:
        task.completed_at = datetime.now(timezone.utc)
        activity_type = ActivityType.COMPLETED
      elif old_status == TaskStatus.DONE:
        task.completed_at = None
        activity_type = ActivityType.REOPENED
      else:
        activity_type = ActivityType.STATUS_CHANGED
      activities.append(TaskActivity(
        user_id=user.id,
        task_id=task.id,
        activity_type=activity_type,
        field_name='status',
        old_value=old_status.value,
        new_value=new_status.value))
      task.status = new_status
  
  db.session.add_all(activities)
  db.session.commit()
  
  return task

def delete_task(task_id, workspace_id, project_id, user):
  membership = get_workspace_membership(workspace_id, user)
  if membership.role != MemberRole.OWNER:
    raise Unauthorized('You do not have permission to delete tasks')
  
  task = get_task(task_id, workspace_id, project_id, user)
  activity = TaskActivity(user_id=user.id, task_id=task.id, activity_type=ActivityType.DELETED)

  task.status = TaskStatus.ARCHIVED

  db.session.add(activity)
  db.session.commit()
  
  return task


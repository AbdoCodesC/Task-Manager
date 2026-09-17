from db import db
from model import TimeBlock, Task, TaskActivity, Project
from model.task_activity import ActivityType
from model.workspace_member import MemberRole
from utils.workspace_member_helpers import get_workspace_membership
from marshmallow import ValidationError
from schema.time_block_schema import time_block_schema, time_block_update_schema

class TimeBlockServiceError(Exception):
  status_code = 400
  
class NotFound(TimeBlockServiceError):
  status_code = 404
  
class Unauthorized(TimeBlockServiceError):
  status_code = 403
  
def get_time_blocks(task_id, user):
  task = db.session.scalar(db.select(Task).join(Project).where(Task.id == task_id, Project.id == Task.project_id))
  if not task:
    raise NotFound("Task not found")

  # any member can see time blocks. 
  get_workspace_membership(task.project.workspace_id, user)
  # if membership.role != MemberRole.OWNER:
  #   raise TimeBlockServiceError('You do not have permission to view time blocks')
  
  return db.session.scalars(db.select(TimeBlock).where(TimeBlock.task_id == task_id).order_by(TimeBlock.start_time.asc())).all()

def create_time_block(task_id, user, data):
  if not data:
    raise TimeBlockServiceError('No data provided')
  
  task = db.session.scalar(db.select(Task).join(Project).where(Task.id == task_id, Project.id == Task.project_id))
  if not task:
    raise NotFound("Task not found or this task does not belong to this project")
  
  membership = get_workspace_membership(task.project.workspace_id, user)
  if membership.role not in [MemberRole.OWNER, MemberRole.ADMIN]:
    raise Unauthorized("You do not have permission to create a time block")
  
  title = (data.get('title') or '').strip()
  start_time = data.get('start_time')
  end_time = data.get('end_time')
  
  if end_time and start_time and end_time <= start_time:
    raise TimeBlockServiceError("End time must be after start time")
  
  errors = time_block_schema.validate({
    'title': title,
    'start_time': start_time,
    'end_time': end_time,
    'task_id': task_id,
  })
  if errors:
    raise ValidationError(errors)
  
  time_block = TimeBlock(title=title, start_time=start_time, end_time=end_time, task_id=task_id)
  
  db.session.add(time_block)
  db.session.flush()
  
  activity = TaskActivity(task_id=task_id, user_id=user.id, activity_type=ActivityType.TIME_BLOCK_ADDED)
  db.session.add(activity)
  
  db.session.commit()
  
  return time_block
  

def update_time_block(time_block_id, task_id, user, data):
  if not data:
    raise TimeBlockServiceError('No data provided')
  
  task = db.session.scalar(db.select(Task).join(Project).where(Task.id == task_id, Project.id == Task.project_id))
  if not task:
    raise NotFound("Task not found")
  
  membership = get_workspace_membership(task.project.workspace_id, user)
  if membership.role not in [MemberRole.OWNER, MemberRole.ADMIN]:
    raise Unauthorized("You do not have permission to update time block")
  
  errors = time_block_update_schema.validate(data)
  if errors:
    raise ValidationError(errors)
  
  time_block = db.session.scalar(db.select(TimeBlock).where(TimeBlock.id == time_block_id, TimeBlock.task_id == task_id))
  if not time_block:
    raise NotFound('Time block not found')
  
  old_start = time_block.start_time
  old_end = time_block.end_time
  
  if 'title' in data:
    time_block.title = data['title'].strip()
  if 'start_time' in data:
    time_block.start_time = data['start_time']
  if 'end_time' in data:
    time_block.end_time = data['end_time']
  
  if time_block.start_time and time_block.end_time and time_block.end_time <= time_block.start_time:
    raise TimeBlockServiceError('End time must be after start time')
    
  activity = TaskActivity(
      task_id=task_id,
      user_id=user.id,
      activity_type=ActivityType.UPDATED,
      field_name='time_block',
      old_value=(f'{old_start} - {old_end}'),
      new_value=(f'{time_block.start_time} - {time_block.end_time}'),
    )

  db.session.add(activity)
  db.session.commit()
    
  return time_block
  

def delete_time_block(time_block_id, task_id, user):
  task = db.session.scalar(db.select(Task).join(Project).where(Task.id == task_id, Project.id == Task.project_id))

  if not task:
    raise NotFound("Task not found")

  membership = get_workspace_membership(task.project.workspace_id, user)
  if membership.role not in [MemberRole.OWNER, MemberRole.ADMIN]:
    raise Unauthorized('You do not have permission to delete time block')

  time_block = db.session.scalar(db.select(TimeBlock).where(TimeBlock.id == time_block_id, TimeBlock.task_id == task_id))
  if not time_block:
    raise NotFound("Time block not found")
  
  activity = TaskActivity(
    task_id=task_id,
    user_id=user.id,
    activity_type=ActivityType.DELETED,
    field_name='time_block',
    details={
      'time_block_id': str(time_block.id),
      'title': time_block.title,
      'start_time': time_block.start_time.isoformat() if time_block.start_time else None,
      'end_time': time_block.end_time.isoformat() if time_block.end_time else None,
    }
  )
  
  db.session.add(activity)
  db.session.delete(time_block)
  db.session.commit()
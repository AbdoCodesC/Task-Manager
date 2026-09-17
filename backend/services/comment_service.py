from db import db
from model import Comment, Project, Task, WorkspaceMember
from model.workspace_member import MemberRole
from model.task_activity import ActivityType, TaskActivity
from schema import comment_schema, comment_update_schema
from marshmallow import ValidationError
from utils.workspace_member_helpers import get_workspace_membership

class CommentServiceError(Exception):
  status_code = 400
  
class NotFound(CommentServiceError):
  status_code = 404
  
class Unauthorized(CommentServiceError):
  status_code = 403

def get_accessible_task(task_id, user):
  if not user or not user.id:
    raise Unauthorized("User not authorized")

  task = db.session.scalar(
    db.select(Task)
    .join(Project, Project.id == Task.project_id)
    .join(
      WorkspaceMember,
      WorkspaceMember.workspace_id == Project.workspace_id,
    )
    .where(
      Task.id == task_id,
      WorkspaceMember.user_id == user.id,
    )
  )

  if not task:
    raise NotFound("Task not found or access denied")

  return task
  
def get_comments(task_id, user):
  get_accessible_task(task_id, user)
  
  return db.session.scalars(db.select(Comment).where(Comment.task_id == task_id).order_by(Comment.created_at.desc())).all()
  

def create_comment(task_id, user, data):  
  if not data:
    raise CommentServiceError('Data not provided')
  
  get_accessible_task(task_id, user)
  
  message = (data.get('message') or '').strip()
  errors = comment_schema.validate({'message': message, 'task_id': task_id, 'user_id': user.id})
  if errors:
    raise ValidationError(errors)
  
  comment = Comment(message=message, task_id=task_id, user_id=user.id)
  
  activity = TaskActivity(task_id=task_id, user_id=user.id, activity_type=ActivityType.COMMENTED)
  
  db.session.add(comment)
  db.session.add(activity)
  db.session.commit()
  
  return comment

def update_comment(comment_id, user, data):
  if not user or not user.id:
    raise Unauthorized('User not authorized')
  
  if not data:
    raise CommentServiceError('Data not provided')
  
  if "message" not in data:
    raise CommentServiceError("Message is required")
  
  errors = comment_update_schema.validate(data)
  if errors:
    raise ValidationError(errors)
  
  comment = db.session.scalar(db.select(Comment).join(Task, Task.id == Comment.task_id).join(Project, Project.id == Task.project_id).join(WorkspaceMember, WorkspaceMember.workspace_id == Project.workspace_id).where(Comment.id == comment_id, Comment.user_id == user.id, WorkspaceMember.user_id == user.id))
  if not comment:
    raise NotFound('Comment not found or you do not have permission')
  
  old_comment = comment.message
  new_comment = data['message'].strip()
  
  if new_comment == old_comment:
    return comment
  
  comment.message = new_comment
  
  activity = TaskActivity(
    task_id=comment.task_id, 
    user_id=user.id, 
    field_name='message',
    old_value=old_comment,
    new_value=new_comment,
    details={"comment_id": str(comment.id)},
    activity_type=ActivityType.UPDATED)
    
  db.session.add(activity)
  db.session.commit()
  
  return comment

def delete_comment(comment_id, user):
  if not user or not user.id:
    raise Unauthorized('User not authorized')

  comment = db.session.scalar(db.select(Comment).where(Comment.id == comment_id))
  if not comment:
    raise NotFound('Comment not found')

  membership = get_workspace_membership(comment.task.project.workspace_id, user)
  can_delete = comment.user_id == user.id or membership.role in [MemberRole.OWNER, MemberRole.ADMIN]
  if not can_delete:
    raise Unauthorized("You can only modify your own comments")
  
  activity = TaskActivity(
    task_id=comment.task_id, 
    user_id=user.id, 
    field_name='message',
    details={
      'comment_id': comment_id,
      "message": comment.message,
      },
    activity_type=ActivityType.DELETED)
    
  db.session.add(activity)
  db.session.delete(comment)
  db.session.commit()
  
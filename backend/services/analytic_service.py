from db import db
from sqlalchemy import func
from model import Comment, Project, Task, TimeBlock
from model.task import TaskStatus
from utils.workspace_member_helpers import get_workspace_membership
from services.workspace_member_service import Unauthorized as MembershipUnauthorized

class AnalyticServiceError(Exception):
  status_code = 400
  
class Unauthorized(AnalyticServiceError):
  status_code = 403

def get_analytics(user, workspace_id):
  if not user or not user.id:
    raise Unauthorized("User not authorized")

  try:
    get_workspace_membership(workspace_id, user)
  except MembershipUnauthorized as error:
    raise Unauthorized(str(error)) from error
  
  project_ids = db.select(Project.id).where(Project.workspace_id == workspace_id)
  task_scope = Task.project_id.in_(project_ids)
  
  total_tasks = db.session.scalar(db.select(func.count(Task.id)).where(task_scope)) or 0
  completed_tasks = db.session.scalar(db.select(func.count(Task.id)).where(task_scope, Task.status == TaskStatus.DONE)) or 0
  total_projects = db.session.scalar(db.select(func.count(Project.id)).where(Project.workspace_id == workspace_id)) or 0
  # Tasks still not finished.
  active_projects = db.session.scalar(db.select(func.count(func.distinct(Project.id))).join(Task, Task.project_id == Project.id).where(Project.workspace_id == workspace_id, Task.status != TaskStatus.ARCHIVED)) or 0
  total_comments = db.session.scalar(db.select(func.count(Comment.id)).join(Task, Task.id == Comment.task_id).join(Project, Project.id == Task.project_id).where(Project.workspace_id == workspace_id)) or 0
  total_focus_seconds = db.session.scalar(db.select(
    func.coalesce(func.sum(func.extract('epoch', TimeBlock.end_time - TimeBlock.start_time), 0))).
    join(Task, Task.id == TimeBlock.task_id).join(Project, Project.id == Task.project_id).
    where(Project.workspace_id == workspace_id, TimeBlock.start_time.isnot(None), TimeBlock.end_time.isnot(None))) or 0
  
  status_rows = db.session.scalars(db.select(Task.status, func.count(Task.id)).where(task_scope).order_by(Task.status)).all()
  priority_rows = db.session.scalars(db.select(Task.priority, func.count(Task.id)).where(task_scope).order_by(Task.priority)).all()
  project_rows = db.session.scalars(db.select(Project.id, Project.name, func.count(Task.id)).
                                    join(Task, Project.id == Task.project_id, isouter=True).
                                    where(Project.workspace_id == workspace_id).
                                    group_by(Project.id, Project.name).
                                    order_by(Project.name)).all()
  
  return {
    'summary': {
      'total_tasks': total_tasks,
      'completed_tasks': completed_tasks,
      'total_projects': total_projects,
      'active_project_count': active_projects,
      'total_comments': total_comments,
      'focus_minutes': round(float(total_focus_seconds) / 60, 2),
      'completion_rate': round((completed_tasks / total_tasks) * 100, 2) if total_tasks else 0,
    },
    'tasks_by_status': [
      {'status': status.value, 'count': count}
      for status, count in status_rows
    ],
    'tasks_by_priority': [
      {'priority': priority.value, 'count': count}
      for priority, count in priority_rows
    ],
    'tasks_by_project': [
      {'project_id': str(project_id), 'project_name': name, 'count': count}
      for project_id, name, count in project_rows
    ],
  }
  
  
  
  
  
  
  
  
  
  






  # project_ids = db.select(Project.id).where(Project.workspace_id == workspace_id)
  # task_scope = Task.project_id.in_(project_ids)

  # total_tasks = db.session.scalar(
  #   db.select(func.count(Task.id)).where(task_scope)
  # ) or 0
  # completed_tasks = db.session.scalar(
  #   db.select(func.count(Task.id)).where(
  #     task_scope,
  #     Task.status == TaskStatus.DONE,
  #   )
  # ) or 0
  # total_projects = db.session.scalar(
  #   db.select(func.count(Project.id)).where(Project.workspace_id == workspace_id)
  # ) or 0
  # active_projects = db.session.scalar(
  #   db.select(func.count(func.distinct(Project.id)))
  #   .join(Task, Task.project_id == Project.id)
  #   .where(
  #     Project.workspace_id == workspace_id,
  #     Task.status != TaskStatus.ARCHIVED,
  #   )
  # ) or 0
  # total_comments = db.session.scalar(
  #   db.select(func.count(Comment.id))
  #   .join(Task, Task.id == Comment.task_id)
  #   .join(Project, Project.id == Task.project_id)
  #   .where(Project.workspace_id == workspace_id)
  # ) or 0
  # total_focus_seconds = db.session.scalar(
  #   db.select(func.coalesce(func.sum(
  #     func.extract('epoch', TimeBlock.end_time - TimeBlock.start_time)
  #   ), 0))
  #   
  # 
  #   .join(Task, Task.id == TimeBlock.task_id)
  #   .join(Project, Project.id == Task.project_id)
  #   .where(
  #     Project.workspace_id == workspace_id,
  #     TimeBlock.start_time.is_not(None),
  #     TimeBlock.end_time.is_not(None),
  #   )
  # ) or 0

  # status_rows = db.session.execute(
  #   db.select(Task.status, func.count(Task.id))
  #   .where(task_scope)
  #   .group_by(Task.status)
  # ).all()
  # priority_rows = db.session.execute(
  #   db.select(Task.priority, func.count(Task.id))
  #   .where(task_scope)
  #   .group_by(Task.priority)
  # ).all()
  # project_rows = db.session.execute(
  #   db.select(Project.id, Project.name, func.count(Task.id))
  #   .join(Task, Task.project_id == Project.id, isouter=True)
  #   .where(Project.workspace_id == workspace_id)
  #   .group_by(Project.id, Project.name)
  #   .order_by(Project.name)
  # ).all()

  # return {
  #   'summary': {
  #     'total_tasks': total_tasks,
  #     'completed_tasks': completed_tasks,
  #     'total_projects': total_projects,
  #     'active_project_count': active_projects,
  #     'total_comments': total_comments,
  #     'focus_minutes': round(float(total_focus_seconds) / 60, 2),
  #     'completion_rate': round((completed_tasks / total_tasks) * 100, 2) if total_tasks else 0,
  #   },
  #   'tasks_by_status': [
  #     {'status': status.value, 'count': count}
  #     for status, count in status_rows
  #   ],
  #   'tasks_by_priority': [
  #     {'priority': priority.value, 'count': count}
  #     for priority, count in priority_rows
  #   ],
  #   'tasks_by_project': [
  #     {'project_id': str(project_id), 'project_name': name, 'count': count}
  #     for project_id, name, count in project_rows
  #   ],
  # }
from db import db
from model import Project
from model.project import ProjectStatus
from model.workspace_member import MemberRole
from schema import project_schema, project_update_schema
from marshmallow import ValidationError
from utils.workspace_member_helpers import get_workspace_membership

class ProjectServiceError(Exception):
  status_code = 400

class Unauthorized(ProjectServiceError):
  status_code = 403

class NotFound(ProjectServiceError):
  status_code = 404
  

def get_projects(workspace_id, user):
  get_workspace_membership(workspace_id, user)
  
  projects = db.session.scalars(db.select(Project).where(Project.workspace_id == workspace_id).order_by(Project.created_at.desc())).all()
  
  return projects

def get_project(workspace_id, project_id, user):
  get_workspace_membership(workspace_id, user)
  project = db.session.scalar(db.select(Project).where(Project.workspace_id == workspace_id, Project.id == project_id))
  if not project:
    raise NotFound('Project not found')
    
  return project
    
def create_project(workspace_id, user, data):
  membership = get_workspace_membership(workspace_id, user)
  
  if membership.role not in [MemberRole.OWNER, MemberRole.ADMIN]:
    raise Unauthorized('You do not have permission to create projects')
  
  if not data:
    raise ProjectServiceError("Data not provided")

  name = (data.get('name') or '').strip()
  description = (data['description'].strip() if data.get('description') is not None else None)
  try:
    status = ProjectStatus(data.get('status', ProjectStatus.TODO.value))
  except ValueError:
    raise ProjectServiceError('Invalid project status')
  
  errors = project_schema.validate({'name': name, 'description': description, 'status': status, 'workspace_id': workspace_id})
  if errors:
    raise ValidationError(errors)
  
  project = Project(name=name, description=description, status=status, workspace_id=workspace_id)
  
  db.session.add(project)
  db.session.commit()
  
  return project

def update_project(workspace_id, project_id, user, data):
  membership = get_workspace_membership(workspace_id, user)
    
  if membership.role not in [MemberRole.OWNER, MemberRole.ADMIN]:
    raise Unauthorized('You do not have permission to update projects')

  if not data:
    raise ProjectServiceError("Data not provided")

  errors = project_update_schema.validate(data)
  if errors:
    raise ValidationError(errors)
  
  project = get_project(workspace_id, project_id, user)
  
  if 'name' in data:
    project.name = data['name'].strip()
  if 'description' in data:
    project.description = (data["description"].strip() if data["description"] is not None else None)
  if 'status' in data:
    project.status = ProjectStatus(data['status'])
  
  db.session.commit()
  
  return project

def delete_project(workspace_id, project_id, user):
  membership = get_workspace_membership(workspace_id, user)
  if membership.role != MemberRole.OWNER:
    raise Unauthorized('Only the workspace owner can delete projects')
  
  project = get_project(workspace_id, project_id, user)
  
  db.session.delete(project)
  db.session.commit()

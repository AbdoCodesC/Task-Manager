from unittest.mock import patch
from types import SimpleNamespace
from model.user import AccountStatus
from model.workspace_member import MemberRole
from model.task import TaskPriority, TaskStatus
from uuid import uuid4

# /<uuid:workspace_id>/projects/<uuid:project_id>/tasks
# /<uuid:workspace_id>/projects/<uuid:project_id>/tasks/<uuid:task_id>

def test_get_tasks(client):
  user = SimpleNamespace(
    id=uuid4(),
    token_version=0,
    account_status=AccountStatus.ACTIVE,
    to_dict=lambda: {'id': 'test-user', 'email': 'user@example.com'}
  )
  with patch('routes.auth.authenticate_user', return_value=user):
    login = client.post('/api/auth/login', json={
      'email': 'user@example.com',
      'password': 'Passwordvalid1!'
    })
  assert login.status_code == 200
  
  task = SimpleNamespace(
    id=uuid4(),
    to_dict=lambda: {'id': 'task-id', 'title': 'Test task'}
  )
  workspace_id = uuid4()
  project_id = uuid4()
  scalars_result = SimpleNamespace(all=lambda: [task])
  auth_result = SimpleNamespace(scalar_one_or_none=lambda: user)
  with patch('app.db.session.get', return_value=user), patch(
    'utils.auth_helpers.db.session.execute', return_value=auth_result
  ), patch('services.task_service.get_workspace_membership'), patch(
    'services.task_service.get_project_in_workspace'
  ), patch(
    'services.task_service.db.session.scalars', return_value=scalars_result
  ):
    response = client.get(
      f'/api/workspaces/{workspace_id}/projects/{project_id}/tasks'
    )
  
  assert response.status_code == 200
  assert response.json == {
    'tasks': [
      {'id': 'task-id', 'title': 'Test task'},
    ]
  }
  
  
def test_create_task(client):
  user = SimpleNamespace(
    id=uuid4(),
    token_version=0,
    account_status=AccountStatus.ACTIVE,
    to_dict=lambda: {'id': 'test-user', 'email': 'user@example.com'}
  )
  with patch('routes.auth.authenticate_user', return_value=user):
    login = client.post('/api/auth/login', json={
      'email': 'user@example.com',
      'password': 'Passwordvalid1!'
    })
  assert login.status_code == 200
  
  csrf_token = client.get_cookie('csrf_access_token').value

  workspace_id = uuid4()
  project_id = uuid4()
  
  membership = SimpleNamespace(
    id=uuid4(),
    workspace_id=workspace_id,
    project_id=project_id,
    role=MemberRole.OWNER,
    to_dict={'id': uuid4(), 'workspace_id': workspace_id,'project_id': project_id, 'role': MemberRole.OWNER}
  )
  
  fake_task = SimpleNamespace(
    to_dict=lambda: {
        "id": "task-id",
        "title": "Help user",
        "description": "Help user 1 do his hw",
        "priority": "low",
        "status": "todo",
    })
  
  auth_result = SimpleNamespace(scalar_one_or_none=lambda: user)
  with patch('app.db.session.get', return_value=user), patch(
    'utils.auth_helpers.db.session.execute', return_value=auth_result
  ), patch('services.task_service.get_workspace_membership', return_value=membership), patch(
    'services.task_service.get_project_in_workspace'
  ), patch(
    'routes.tasks.create_task', return_value=fake_task
  ):
    response = client.post(
      f'/api/workspaces/{workspace_id}/projects/{project_id}/tasks', 
      json={
          "title": "Help user",
          "description": "Help user 1 do his hw",
          "priority": "low",
          "status": "todo",
      },
      headers={
        'X-CSRF-TOKEN': csrf_token
      }
    )
  
  assert response.status_code == 201
  assert response.json["task"]["title"] == "Help user"
  assert response.json["task"]["priority"] == "low"
  assert response.json["task"]["status"] == "todo"
  
def test_delete_task(client):
  user = SimpleNamespace(
    id=uuid4(),
    token_version=0,
    account_status=AccountStatus.ACTIVE,
    to_dict=lambda: {'id': 'test-user', 'email': 'user@example.com'}
  )
  with patch('routes.auth.authenticate_user', return_value=user):
    login = client.post('/api/auth/login', json={
      'email': 'user@example.com',
      'password': 'Passwordvalid123!'
    })
  
  assert login.status_code == 200
  
  csrf_token = client.get_cookie('csrf_access_token').value
  
  task_id = uuid4()
  workspace_id = uuid4()
  project_id = uuid4()
  
  membership = SimpleNamespace(
    id=uuid4(),
    workspace_id=workspace_id,
    project_id=project_id,
    role=MemberRole.OWNER,
    to_dict={'id': uuid4(), 'workspace_id': workspace_id,'project_id': project_id, 'role': MemberRole.OWNER}
  )
  
  fake_task = SimpleNamespace(
    id=uuid4(),
    status=TaskStatus.TODO,
    to_dict=lambda: {
      "id": "task-id",
      "title": "Help user",
      "description": "Help user 1 do his hw",
      "priority": "low",
      "status": "todo",
    })
  
  auth_user = SimpleNamespace(scalar_one_or_none=lambda: user)
  with patch('app.db.session.get', return_value=user), patch('utils.auth_helpers.db.session.execute', return_value=auth_user), patch('services.workspace_member_service.get_workspace_membership', return_value=membership), patch('services.task_service.get_project_in_workspace'), patch('routes.tasks.delete_task', return_value=fake_task):
    response = client.delete(f'/api/workspaces/{workspace_id}/projects/{project_id}/tasks/{task_id}',
                             headers={'X-CSRF-TOKEN': csrf_token})
    
  assert response.status_code == 204
  assert response.data == b''
  
    
    
  
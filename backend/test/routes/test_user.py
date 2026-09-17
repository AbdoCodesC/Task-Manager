from types import SimpleNamespace
from uuid import uuid4
from unittest.mock import patch
from model.user import AccountStatus

def test_get_profile(client):
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
  result = SimpleNamespace(scalar_one_or_none=lambda: user)
  with patch('app.db.session.get', return_value=user), patch(
    'utils.auth_helpers.db.session.execute', return_value=result
  ):
    response = client.get('/api/users/me')
    
  assert response.status_code == 200
  assert response.json['user'] == {
    'id': 'test-user',
    'email': 'user@example.com',
  }

def test_update_account(client):
  user = SimpleNamespace(
      id=uuid4(),
      first_name='Abdeer',
      last_name='Chaibe',
      email='abdo23@gmail.com',
      password='Passisvalid123!',
      token_version=0,
      account_status=AccountStatus.ACTIVE,
      to_dict=lambda: {
        'id': 'test-user',
        'full_name': f'{user.first_name} {user.last_name}',
        'email': user.email,
        'password': user.password
      }
    )
    
  with patch('routes.auth.authenticate_user', return_value=user):
      login = client.post('/api/auth/login', json={
        'email': 'user@example.com',
        'password': 'Passwordvalid1!'
      })
      
  csrf_token = client.get_cookie('csrf_access_token').value
  
  assert login.status_code == 200
  result = SimpleNamespace(scalar_one_or_none=lambda: user)
  with patch('app.db.session.get', return_value=user), patch(
    'utils.auth_helpers.db.session.execute', return_value=result
  ):
    response = client.patch('/api/users/me', headers={'X-CSRF-TOKEN': csrf_token}, json={
      'first_name': 'Abdo',
      'email': 'abdo23@gmail.com',
      'password': 'Passisvalid123!'
    })
    
  assert response.status_code == 200
  assert response.json['user']['full_name'] == 'Abdo Chaibe'
  assert response.json['user']['email'] == 'abdo23@gmail.com'
  assert response.json['user']['password'] == 'Passisvalid123!'

def test_delete_account(client):
  user = SimpleNamespace(
    id=uuid4(),
    token_version=0,
    account_status=AccountStatus.ACTIVE,
    deleted_at=None,
    to_dict=lambda: {'id': 'test-user', 'email': 'user@example.com', 'account_status': user.account_status, 'delete_at': user.deleted_at}
  )
  
  with patch('routes.auth.authenticate_user', return_value=user):
    login = client.post('/api/auth/login', json={
      'email': 'user@example.com',
      'password': 'Passwordvalid1!'
    })
    
  csrf_token = client.get_cookie('csrf_access_token').value
  
  assert login.status_code == 200
  result = SimpleNamespace(scalar_one_or_none=lambda: user)
  
  with patch('app.db.session.get', return_value=user), patch(
    'utils.auth_helpers.db.session.execute', return_value=result
  ):
    response = client.delete('/api/users/me', headers={'X-CSRF-TOKEN': csrf_token})
  
  assert response.status_code == 204
  assert response.data == b""
  assert user.account_status == AccountStatus.DELETED
  assert user.deleted_at is not None
  
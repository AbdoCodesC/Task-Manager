from types import SimpleNamespace
from unittest.mock import patch
from uuid import uuid4

# Credentials

def test_login_sets_auth_cookies(client):
  user = SimpleNamespace(
      id=uuid4(),
      token_version=0,
      to_dict=lambda: {
          "id": "test-user",
          "email": "user@example.com",
      },
  )

  with patch("routes.auth.authenticate_user", return_value=user) as authenticate:
    response = client.post(
      "/api/auth/login",
      json={
        "email": "user@example.com",
        "password": "ValidPassword1!",
      },
    )

  assert response.status_code == 200
  assert response.json["message"] == "User logged in successfully"
  assert response.json["user"]["email"] == "user@example.com"
  set_cookie_headers = response.headers.getlist("Set-Cookie")
  assert any("access_token_cookie" in value for value in set_cookie_headers)
  assert any("refresh_token_cookie" in value for value in set_cookie_headers)
  authenticate.assert_called_once_with(
    {
      "email": "user@example.com",
      "password": "ValidPassword1!",
    }
  )


def test_login_rejects_invalid_credentials(client):
  from services.auth_service import InvalidCredentials

  with patch(
      "routes.auth.authenticate_user",
      side_effect=InvalidCredentials("Invalid email or password"),
  ):
      response = client.post(
          "/api/auth/login",
          json={
              "email": "user@example.com",
              "password": "wrong-password",
          },
      )

  assert response.status_code == 401
  assert response.json == {"error": "Invalid email or password"}

def test_signup(client):
  user = SimpleNamespace(
    id=uuid4(),
    token_version=0,
    to_dict=lambda: {'id': 'test-user', 'email': 'user@example.com'},
  )
  workspace = SimpleNamespace(
    to_dict=lambda: {'name': "Abdo's Workspace"},
  )

  with patch('routes.auth.create_user', return_value=(user, workspace)):
    response = client.post('/api/auth/signup', json={
      'first_name': 'Abdo',
      'last_name': 'Chaibe',
      'email': 'user@example.com',
      'password': 'ValidPassword1!',
    })
  
  assert response.status_code == 201
  assert response.json['message'] == 'User signed up successfully'
  assert response.json['user']['email'] == 'user@example.com'
  assert response.json['workspace']['name'] == "Abdo's Workspace"
  set_cookie_headers = response.headers.getlist('Set-Cookie')
  assert any('access_token_cookie' in cookie for cookie in set_cookie_headers)
  assert any('refresh_token_cookie' in cookie for cookie in set_cookie_headers)

# Rate limit
def test_login_rate_limit(rate_client):
  for _ in range(5):
    rate_client.post('/api/auth/login', json={
      'email': 'user@example.com',
      'password': 'wrong'
    })
  
  response = rate_client.post('/api/auth/login', json={
    'email': 'user@example.com',
    'password': 'wrong'
  })
  
  assert response.status_code == 429
  
def test_signup_rate_limit(rate_client):
  for _ in range(4):
    rate_client.post('/api/auth/signup', json={
      'first_name': 'Abdo',
      'last_name': 'Chaibe',
      'email': 'user@example.com',
      'password': 'wrong'
    })
  
  response = rate_client.post('/api/auth/signup', json={
    'first_name': 'Abdo',
    'last_name': 'Chaibe',
    'email': 'user@example.com',
    'password': 'wrong'
  })
  
  assert response.status_code == 429
  
def test_logout_rejects_reused_token(rate_client):
  user = SimpleNamespace(
    id=uuid4(),
    token_version=0,
    to_dict=lambda: {'id': 'test-user', 'email': 'user@example.com'},
  )

  with patch('routes.auth.authenticate_user', return_value=user):
    login_response = rate_client.post("/api/auth/login", json={
      "email": "user@example.com",
      "password": "ValidPassword1!",
    })

  csrf_token = rate_client.get_cookie('csrf_access_token').value
  with patch('app.db.session.get', return_value=user):
    first_logout = rate_client.post(
      '/api/auth/logout',
      headers={'X-CSRF-TOKEN': csrf_token},
    )
    second_logout = rate_client.post(
      '/api/auth/logout',
      headers={'X-CSRF-TOKEN': csrf_token},
    )

  assert first_logout.status_code == 200
  assert second_logout.status_code == 401
  

# logout
def test_logout(client):
  user = SimpleNamespace(
    id=uuid4(),
    token_version=0,
    to_dict=lambda: {'id': 'test-user', 'email': 'user@example.com'},
  )

  with patch('routes.auth.authenticate_user', return_value=user):
    login_response = client.post("/api/auth/login", json={
        "email": "user@example.com",
        "password": "ValidPassword1!",
      })
  assert login_response.status_code == 200

  csrf_token = client.get_cookie('csrf_access_token').value
  with patch('app.db.session.get', return_value=user):
    logout_response = client.post(
      '/api/auth/logout',
      headers={'X-CSRF-TOKEN': csrf_token},
    )
  
  assert logout_response.status_code == 200
  set_cookie_headers = logout_response.headers.getlist('Set-Cookie')
  assert any('access_token_cookie=' in value for value in set_cookie_headers)
  assert any('refresh_token_cookie=' in value for value in set_cookie_headers)
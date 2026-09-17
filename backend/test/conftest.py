import pytest
from uuid import uuid4
from app import create_app


@pytest.fixture()
def app():
  app = create_app()
  app.config.update(
    TESTING=True,
    RATELIMIT_ENABLED=False,
    JWT_COOKIE_SECURE=False,
    )
  
  yield app
  
@pytest.fixture()
def client(app):
  with app.test_client() as client:
    client.environ_base['REMOTE_ADDR'] = f'203.0.113.{uuid4().int % 254 + 1}'
    yield client

@pytest.fixture()
def rate_client():
  app = create_app()
  app.config.update(
    TESTING=True,
    RATELIMIT_ENABLED=True,
    JWT_COOKIE_SECURE=False,
  )

  with app.test_client() as client:
    client.environ_base['REMOTE_ADDR'] = f'198.51.100.{uuid4().int % 254 + 1}'
    yield client
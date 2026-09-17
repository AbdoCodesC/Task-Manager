from flask import has_request_context
from flask_limiter.util import get_remote_address
from flask_jwt_extended import get_jwt_identity

def rate_limit_key():
  if has_request_context():
    try:
      identity = get_jwt_identity()
      if identity:
        return f"user:{identity}"
    except RuntimeError:
      pass
  return f"ip:{get_remote_address()}"
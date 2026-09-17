from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_limiter import Limiter
from utils.rate_limit_key import rate_limit_key
import os
import dotenv
dotenv.load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
if not REDIS_HOST or not REDIS_PORT:
  raise RuntimeError("Missing redis host or port")

ma = Marshmallow()
bcrypt = Bcrypt()
migrate = Migrate()
jwt_manager = JWTManager()

limiter = Limiter(key_func=rate_limit_key, default_limits=['300 per minute'], storage_uri=f'redis://{REDIS_HOST}:{REDIS_PORT}/1')

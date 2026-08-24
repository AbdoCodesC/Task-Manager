from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

ma = Marshmallow()
bcrypt = Bcrypt()
migrate = Migrate()
jwt_manager = JWTManager()
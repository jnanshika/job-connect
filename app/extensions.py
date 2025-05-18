from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from authlib.integrations.flask_client import OAuth
from flask_migrate import Migrate
from flasgger import Swagger

db = SQLAlchemy()
jwt = JWTManager()
oauth = OAuth()
migrate = Migrate()
swagger = Swagger()
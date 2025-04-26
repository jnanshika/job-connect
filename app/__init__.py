from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from authlib.integrations.flask_client import OAuth

db = SQLAlchemy()
jwt = JWTManager()
oauth = OAuth()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    jwt.init_app(app)
    oauth.init_app(app)

    # Import and register blueprints here
    from app.routes.auth_routes import auth_bp
    from app.routes.job_routes import job_bp
    from app.routes.application_routes import application_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(job_bp)
    app.register_blueprint(application_bp)

    return app

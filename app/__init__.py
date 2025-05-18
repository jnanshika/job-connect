from flask import Flask
from app.extensions import db, jwt, migrate, swagger
from app.routes import register_routes
from yaml import safe_load
import os
from deepmerge import always_merger

def create_app():
    app = Flask(__name__)
    
    # Configurations
    app.config.from_object('app.config.Config')  # Load the configuration
    
    db.init_app(app)  # Initialize the database with the app
    migrate.init_app(app, db)
    
    # Register Routes (This will register all routes from your routes directory)
    register_routes(app)
    
    #Load external swagger yml template
    # yaml_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'docs', 'users.yml'))
    # with open(yaml_path, 'r') as f:
    #     template = safe_load(f)

    # swagger.template = template
    docs_path = os.path.join(os.path.dirname(__file__), 'docs')
    combined_template = {}

    for filename in ['users.yml', 'jobs.yml', 'applications.yml']:
        with open(os.path.join(docs_path, filename)) as f:
            data = safe_load(f)
            always_merger.merge(combined_template, data)

    swagger.template = combined_template

    swagger.init_app(app) # initialise after routes
    jwt.init_app(app)

    # Create all tables in the database (Will create tables for all models)
    with app.app_context():
        db.create_all()

    @app.route('/')
    def home():
        return 'Setup is ready!'  # Basic home route 
    
    return app

from flask import Flask
from app.extensions import db, jwt
from app.routes import register_routes

def create_app():
    app = Flask(__name__)
    
    # Configurations
    app.config.from_object('app.config.Config')  # Load the configuration
    db.init_app(app)  # Initialize the database with the app

    # Register Routes (This will register all routes from your routes directory)
    register_routes(app)
    jwt.init_app(app)

    # Create all tables in the database (Will create tables for all models)
    with app.app_context():
        db.create_all()

    @app.route('/')
    def home():
        return 'Setup is ready!'  # Basic home route to check if the app is working
    
    return app

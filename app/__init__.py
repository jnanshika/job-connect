from flask import Flask
from app.extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    db.init_app(app)

    @app.route('/')
    def home():
        return 'Setup is ready!'

    return app

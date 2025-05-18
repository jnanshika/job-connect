#Central place for app configuration (database URI, OAuth secrets).
import os
from dotenv import load_dotenv
 
load_dotenv()  # load .env into environment variable

class Config:
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv( "DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.getenv("FLASK_ENV") == "developement"
    SWAGGER = {
        'title': 'Job Connect API',
        'uiversion': 3,
        'swagger': '2.0',
        'specs_route': '/apidocs/',
        'specs': [{
            'endpoint': 'apispec',
            'route': '/apispec.json',
            'rule_filter': lambda rule: True,  # all rules
            'model_filter': lambda tag: True,  # all models
        }],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True
    }
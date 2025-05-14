#Central place for app configuration (database URI, OAuth secrets).
import os
from dotenv import load_dotenv
 
load_dotenv()  # load .env into environment variable

class Config:
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv( "DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.getenv("FLASK_ENV") == "development"
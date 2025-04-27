#Central place for app configuration (database URI, OAuth secrets).

class Config:
    SECRET_KEY = 'somethingsecret'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # or any db you want
    SQLALCHEMY_TRACK_MODIFICATIONS = False


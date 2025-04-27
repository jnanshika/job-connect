#Central place for app configuration (database URI, OAuth secrets).

class Config:
    SECRET_KEY = 'eZgaF9ESATNIyshm78i9'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # or any db you want
    SQLALCHEMY_TRACK_MODIFICATIONS = False


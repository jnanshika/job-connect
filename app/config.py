#Central place for app configuration (database URI, OAuth secrets).
import os

class Config:
    SECRET_KEY = 'eZgaF9ESATNIyshm78i9'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "mysql+pymysql://root:root@localhost:3306/jobconnect"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
"""So when you initialize your app (like in app/__init__.py), you don't have to manually import models everywhere.
It registers all models once.
"""

from .user import UserModel
from .job import JobModel
from .application import ApplicationModel

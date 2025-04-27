from .user_routes import user_routes
from .job_routes import job_routes
from .application_routes import application_routes

def register_routes(app):
    app.register_blueprint(user_routes, url_prefix='/users')
    app.register_blueprint(job_routes, url_prefix='/jobs')
    app.register_blueprint(application_routes, url_prefix='/applications')

from flask import Blueprint, request
from app.models import ApplicationModel
from app.schemas import ApplicationSchema, ValidationError
from app.extensions import db

application_routes = Blueprint('application_routes', __name__)

@application_routes.route('/apply', methods=['POST'])
def apply_job():
    jsondata = request.get_json()
    
    # Validate input data
    """errors = application_schema.validate(data) 
    if errors:
        return {"message": errors}, 400"""
    try:
        application_schema = ApplicationSchema()
        application_object = application_schema.load(jsondata)
    
    except ValidationError as error:
        return {"errors": error.messages}, 400

    # Create application
    application = ApplicationModel(
        user_id=application_object['user_id'],
        job_id=application_object['job_id'],
        status=application_object['status']
    )
    db.session.add(application)
    db.session.commit()

    return application_schema.dump(application), 201

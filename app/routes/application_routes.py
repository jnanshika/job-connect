from flask import Blueprint, request
from app.models import ApplicationModel
from app.schemas import ApplicationSchema
from app.extensions import db

application_routes = Blueprint('application_routes', __name__)

@application_routes.route('/apply', methods=['POST'])
def apply_job():
    data = request.get_json()
    application_schema = ApplicationSchema()

    # Validate input data
    errors = application_schema.validate(data)
    if errors:
        return {"message": errors}, 400

    # Create application
    application = ApplicationModel(
        user_id=data['user_id'],
        job_id=data['job_id'],
        status=data['status']
    )
    db.session.add(application)
    db.session.commit()

    return application_schema.dump(application), 201

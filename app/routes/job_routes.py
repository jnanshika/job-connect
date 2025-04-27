from flask import Blueprint, request
from app.models import JobModel
from app.schemas import JobSchema
from app.extensions import db

job_routes = Blueprint('job_routes', __name__)

@job_routes.route('/jobs', methods=['POST'])
def create_job():
    data = request.get_json()
    job_schema = JobSchema()

    # Validate input data
    errors = job_schema.validate(data)
    if errors:
        return {"message": errors}, 400

    # Create job
    job = JobModel(
        title=data['title'],
        description=data['description'],
        location=data['location'],
        posted_by=data['posted_by']
    )
    db.session.add(job)
    db.session.commit()

    return job_schema.dump(job), 201

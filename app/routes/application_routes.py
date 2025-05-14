from flask import Blueprint, request
from app.schemas import ApplicationSchema, ValidationError
from app.extensions import db
from app.models import ApplicationModel, UserModel, JobModel
from app.services import AuthService, ApplicationService
from app.utils import token_required, candidate_required, recruiter_required

application_routes = Blueprint('application_routes', __name__)

@application_routes.route('/create/<int:job_id>', methods=['POST'])
@candidate_required
def create_application(candidate_record, job_id):
    jsonData = request.get_json()
    if not candidate_record or candidate_record.status != 'active':
        return {"error": "Inactive or invalid candidate"}, 403

    job = JobModel.query.filter_by(id= job_id).first()
    if not job or job.status != 'Active' :
        return {"error": "Inactive or invalid job"}, 403

    try: 
        app_schema = ApplicationSchema(session = db.session, partial = True)  #instance of schema
        application = app_schema.load(jsonData)  #Deserialise (json -> JobModel instance)
        application.user_id = candidate_record.id
        application.job_id = job_id

    except ValidationError as error:
        return {"errors": error.messages}, 400

    return ApplicationService.create_application(application)


@application_routes.route('/jobid/<int:job_id>', methods=['GET'])
@recruiter_required
def get_applications(recruiter, job_id):
    job = JobModel.query.get(job_id)
    if not job:
        return {"error": "Job not found"}, 404

    if job.posted_by != recruiter.id:
        return {"error" : f"This job was not posted by {recruiter.name}"}

    applications = ApplicationModel.query.filter_by(job_id = job_id).all()
    if not applications: 
        return {"message", "No application was found"} , 200
    
    try: 
        result = ApplicationSchema(many=True).dump(applications)
        return {"applications": result}, 200    
    except ValidationError as error:
        return {"errors": error.messages}, 400
    
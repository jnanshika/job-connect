from flask import Blueprint, request
from app.schemas import JobSchema, ValidationError
from app.services import JobService, AuthService
from app.models import JobModel, UserModel
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.extensions import db
from app.utils import token_required, candidate_required, recruiter_required, admin_required

job_routes = Blueprint('job_routes', __name__)

@job_routes.route('/create',methods=['POST'])
@recruiter_required
def create_job(user):
    jsonData = request.get_json()
    if 'posted_by' in jsonData :
        return {"message" : "You cannot set posted by is manually"}, 400
    
    try: 
        job_schema = JobSchema(session = db.session)  #instance of schema
        jobData = job_schema.load(jsonData)  #Deserialise (json -> JobModel instance)
        jobData.posted_by = user.id
    except ValidationError as error:
        return {"errors": error.messages}, 400
    
    return JobService.create_job(jobData)


@job_routes.route('/', methods=['GET'])
def get_alljobs():
    jobs = JobModel.query.all()
    if not jobs:
        return {"message": "No jobs found"}, 200
    
    try: 
        job_schema = JobSchema(many= True)
    
    except ValidationError as error:
        return {"errors": error.messages}, 400

    return { "jobs:" :job_schema.dump(jobs) }, 200


@job_routes.route('/update/<int:job_id>', methods=['PATCH'])
@recruiter_required
def update_job(logged_user, job_id):
    curr_jobRecord = JobModel.query.filter_by(id=job_id).first()
    if not curr_jobRecord:
        return {"message": "Job not found"}, 400
    
    #verify logged user posted the job
    if curr_jobRecord.posted_by != logged_user.id:
        return {"message": f"This job was not posted by {logged_user.name}"}, 400
    
    jsonData = request.get_json()

    try: 
        job_schema = JobSchema(session=db.session, partial=True)  #instance of schema
        update_record = job_schema.load(jsonData)  #Deserialise (json -> JobModel instance)
    except ValidationError as error:
        return {"errors": error.messages}, 400
    
    return JobService.update_job(update_record, curr_jobRecord)


@job_routes.route('/<int:job_id>/deactivate', methods =['PATCH'])
@recruiter_required
def deactivate_job(logged_user,job_id):
    job_record = JobModel.query.filter_by(id= job_id).first()
    if not job_record:
        return {"error": f"No job found with ID {job_id}"}, 404
    
    
    if job_record.posted_by != logged_user.id:
        return {"message": f"This job was not posted by {logged_user.name}"}, 400
    return JobService.deactivate_job(job_record)


# @job_routes.route('/<int:job_id>/delete', methods =['DELETE'])
# @admin_required
# def delete_job(user, job_id):
    # job_record = JobModel.query.filter_by(id= job_id).first()
    # if not job_record:
    #     return {"error": f"No job found with ID {job_id}"}, 404
    
    # return JobService.delete_job(job_record)
from flask import Blueprint, request
from app.schemas import JobSchema, ValidationError
from app.services import JobService, user_service
from app.models import JobModel, UserModel
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.extensions import db

job_routes = Blueprint('job_routes', __name__)

@jwt_required()
def verify_recruiter():
    #verify token - if user have access
    message, status = user_service.AuthService.verify_token()
    if status != 200:
        return message, status
    
    #verify is user is a recruiter 
    user_id = get_jwt_identity()
    user = UserModel.query.filter_by(id=user_id).first()

    if user.role != "recruiter":
        return {"message": "User must be a recruiter"}, 403
        
    return {"user": user}, 200

@jwt_required()
def verify_admin():
    #verify token - if user have access
    message, status = user_service.AuthService.verify_token()
    if status != 200:
        return message, status
    
    #verify if user is an admin
    user_id = get_jwt_identity()
    user = UserModel.query.filter_by(id=user_id).first()
    if user.role != "admin":
        return {"message": "User must be an Admin"}, 403
        
    return {"user": user}, 200

@job_routes.route('/',methods=['POST'])
def create_job():
    #only recruiter can create job
    result, status = verify_recruiter() 
    if status!= 200:
        return result, status
    user = result["user"]
    
    #got the json data
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

@job_routes.route('/<int:job_id>', methods=['PATCH'])
def update_job(job_id):
    #verify recruiter
    result, status = verify_recruiter() 
    if status!= 200:
        return result, status
    logged_user = result["user"]

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
def deactivate_job(job_id):
    #verify recruiter
    result, status = verify_recruiter() 
    if status!= 200:
        return result, status
    logged_user = result["user"]
    
    job_record = JobModel.query.filter_by(id= job_id).first()
    if not job_record:
        return {"error": f"No job found with ID {job_id}"}, 404
    
    
    if job_record.posted_by != logged_user.id:
        return {"message": f"This job was not posted by {logged_user.name}"}, 400
    return JobService.deactivate_job(job_record)
    
@job_routes.route('/<int:job_id>/delete', methods =['DELETE'])
def delete_job(job_id):
    #verify admin
    admin_result, admin_status = verify_admin()
    if admin_status != 200:
        return {"message" : "User must be an Admin"}, 400
    
    job_record = JobModel.query.filter_by(id= job_id).first()
    if not job_record:
        return {"error": f"No job found with ID {job_id}"}, 404
    
    return JobService.delete_job(job_record)
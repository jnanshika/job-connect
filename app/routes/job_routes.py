from flask import Blueprint, request
from app.schemas import JobSchema, ValidationError
from app.services import JobService, auth_service
from app.models import JobModel, UserModel
from flask_jwt_extended import get_jwt_identity, jwt_required

job_routes = Blueprint('job_routes', __name__)

@jwt_required()
def verify_recruiter():
    #verify token - if user have access
    message, status = auth_service.AuthService.verify_token()
    if status != 200:
        return message, status
    
    #verify is user is a recruiter 
    user_id = get_jwt_identity()
    user = UserModel.query.filter_by(id=user_id).first()

    if user.role != "recruiter":
        return {"message": "User must be a recruiter"}, 403
        
    return {"user": user}, 200


@job_routes.route('/create',methods=['POST'])
def create():
    #only recruiter can create job
    result, status = verify_recruiter() 
    if status!= 200:
        return result, status
    user = result["user"]
    #got the json data
    jsonData = request.get_json()
    try: 
        job_schema = JobSchema()  #instance of schema

        dictData = job_schema.load(jsonData)  #Deserialise (json -> pyon dict)
    except ValidationError as error:
        return {"errors": error.messages}, 400
    dictData['posted_by'] = user.id
    return JobService.create_job(dictData)


@job_routes.route('/getjobs', methods=['GET'])
def get_alljobs():
    jobs = JobModel.query.all()
    if not jobs:
        return {"message": "No jobs found"}, 200
    
    try: 
        job_schema = JobSchema(many= True)
    
    except ValidationError as error:
        return {"errors": error.messages}, 400

    return { "jobs:" :job_schema.dump(jobs) }, 200

@job_routes.route('/update/<int:job_id>', methods=['PUT'])
def update(job_id):
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
        job_schema = JobSchema()  #instance of schema

        update_record = job_schema.load(jsonData, partial=True)  #Deserialise (json -> pyon dict)
    except ValidationError as error:
        return {"errors": error.messages}, 400
    
    return JobService.update_job(update_record, curr_jobRecord)

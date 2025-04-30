from flask import Blueprint, request
from app.schemas import JobSchema, ValidationError
from app.services import JobService
from app.models import JobModel

job_routes = Blueprint('job_routes', __name__)

@job_routes.route('/create',methods=['POST'])
def create():
    #got the json data
    jsonData = request.get_json()
    try: 
        job_schema = JobSchema()  #instance of schema

        dictData = job_schema.load(jsonData)  #Deserialise (json -> pyon dict)
    except ValidationError as error:
        return {"errors": error.messages}, 400

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

@job_routes.route('/update/<int:id>', methods=['PUT'])
def update(id):

    #TODO : recruiter can update jobs posted by them and only recruiter can update jobs - using user id from session
    curr_record = JobModel.query.filter_by(id=id).first()

    if not curr_record:
        return {"message": "Job not found"}, 200
    
    jsonData = request.get_json()
    try: 
        job_schema = JobSchema()  #instance of schema

        update_record = job_schema.load(jsonData, partial=True)  #Deserialise (json -> pyon dict)
    except ValidationError as error:
        return {"errors": error.messages}, 400
    
    return JobService.update_job(update_record, curr_record)

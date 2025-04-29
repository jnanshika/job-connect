from app.models import UserModel, JobModel
from app.extensions import db

class JobService():

    @staticmethod
    def create_job(data):

        recruiter_id = data['posted_by']
        #check if recruiter exists
        existing_recruiter = UserModel.query.filter_by(id = recruiter_id).first()
        if not existing_recruiter:
            return {"message": "Recruiter not registered"}, 400
        
        #create a new job
        new_job = JobModel(
            title = data['title'],
            description = data['description'],
            posted_by = data['posted_by'],
            location = data['location']
        )

        #add in database
        db.session.add(new_job)
        db.session.commit()

        return {"message": "Job was sccessfully added!"}, 200
    


    @staticmethod
    def update_job(update_record, curr_record):

        """#check if recruiter exists
        job_record = JobModel.query.filter_by(id = record_id).first()
        
        if not job_record:
            return {"message": "Job not found"}, 404"""
        
        for key, value in update_record.items():
            setattr(curr_record, key, value)  # Dynamically update only provided fields

        #add in database
        db.session.add(curr_record)
        db.session.commit()

        return {"message": "Job was sccessfully updated!"}, 200

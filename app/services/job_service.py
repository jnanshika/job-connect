from app.models import UserModel, JobModel
from app.extensions import db
from app.schemas import JobSchema

class JobService():

    @staticmethod
    def create_job(data):
        db.session.add(data)
        db.session.commit()

        return {"message": "Job was sccessfully added!"}, 201

    @staticmethod
    def update_job(update_record : JobModel, curr_record : JobModel):
        # Schema with session for ORM deserialization
        schema = JobSchema(session=db.session)

        # Get all fields that are not dump_only → meaning allowed to be updated
        updatable_fields = [
            field_name
            for field_name, field_obj in schema.fields.items()
            if not field_obj.dump_only
        ]

        # Only update allowed attributes
        for attr in updatable_fields:
            new_value = getattr(update_record, attr, None)
            if new_value is not None:
                setattr(curr_record, attr, new_value)

        db.session.commit()
        return {"message": "Job was successfully updated!"}, 200

    
    #todo -> restrict for admin
    @staticmethod
    def delete_jobs():
        try:
            db.session.query(JobModel).delete()
            db.session.commit()
            return {"message": "All jobs are deleted"}, 200
        
        except Exception as e:
            db.session.rollback()
            return {"error": "Error while deleting jobs"}, 400

    @staticmethod
    def deactivate_job(job_record : JobModel):
        try:
            job_record.status = "InActive"
            db.session.commit()
            return {"message": f"Job with id {job_record.id} was marked as InActive."}, 200
        
        except Exception as e:
            db.session.rollback()
            return {"error": f"Error while marking job as InActive. {str(e)}"}, 400

    def delete_job(job_record):
        try:
            db.session.delete(job_record)
            db.session.commit()
            return {"message": "Job was successfully deleted!"}, 200
        except Exception as e:
            db.session.rollback()
            return {"error": f"Error while deleting job. {str(e)}"}, 400

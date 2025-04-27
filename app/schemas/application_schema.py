from marshmallow import Schema, fields, validates, ValidationError
from marshmallow.validate import Length
from app.models import ApplicationStatus, ApplicationModel, UserModel, JobModel

class ApplicationSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)  # Foreign key to User model
    job_id = fields.Int(required=True)   # Foreign key to Job model
    status = fields.Str(required=True, validate=Length(min=1))
    created_at = fields.DateTime(dump_only=True)

    @validates('status')
    def validate_status(self, value):
        allowed_status = [status.value for status in ApplicationStatus]  # Get the enum values dynamically
        if value not in allowed_status:
            raise ValidationError(f"Status must be one of {allowed_status}")

    @validates('user_id')
    def validate_user_id(self, value):
        user = UserModel.query.filter_by(id=value).first()
        if not user:
            raise ValidationError("User does not exist.")
        if user.role != 'job_seeker':
            raise ValidationError("Only job seekers can apply for jobs.")
    
    @validates('job_id')
    def validate_job_id(self, value):
        job = JobModel.query.filter_by(id=value).first()
        if not job:
            raise ValidationError("Job does not exist.")
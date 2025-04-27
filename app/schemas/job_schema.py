from marshmallow import Schema, fields, validates, ValidationError
from marshmallow.validate import Length
from app.models import JobModel, UserModel

class JobSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=Length(min=10))
    description = fields.Str(required=True, validate=Length(min=10))
    location = fields.Str(required=True, validate=Length(min=10))
    posted_by = fields.Int(required=True)
    created_at = fields.DateTime(dump_only= True)

    @validates('posted_by')
    def posted_by(self, value):
        user = UserModel.query.filter_by(id=value).first()
        if not user:
            raise ValidationError("Recruiter account does not exists.")
        
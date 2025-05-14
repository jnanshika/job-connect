from marshmallow import validate
from marshmallow.validate import Length
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from app.models import JobModel

Valid_JobStatus = ['Active' , 'Inactive', 'Draft', 'Closed']

#Setting load_instance=True tells Marshmallow to return a model instance instead of a plain dictionary.
class JobSchema(SQLAlchemySchema):
    class Meta:
        model = JobModel
        load_instance = True  #gives you a JobModel instance

    id = auto_field(dump_only=True)
    title = auto_field(required=True, validate=Length(min=5))
    description = auto_field(required=True, validate=Length(min=5))
    location = auto_field(required=True, validate=Length(min=3))
    status = auto_field(required=True, validate=validate.OneOf(Valid_JobStatus))  
    posted_by = auto_field(dump_only=True)  
    created_at = auto_field(dump_only=True)
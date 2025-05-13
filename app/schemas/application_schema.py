from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from app.models import ApplicationModel  # adjust import path if needed

class ApplicationSchema(SQLAlchemySchema):
    class Meta:
        model = ApplicationModel
        load_instance = True
        include_fk = True  # includes foreign key fields like user_id, job_id

    id = auto_field(dump_only=True)
    user_id = auto_field(dump_only=True)
    job_id = auto_field(dump_only=True)
    status = auto_field(required=True)
    resume = auto_field(required=False)
    applied_on = auto_field(dump_only=True)

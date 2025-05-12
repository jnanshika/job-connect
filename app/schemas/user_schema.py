from marshmallow import Schema, fields, validates, ValidationError
from marshmallow.validate import Length, Email
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from app.models import UserModel

VALID_ROLES = ['candidate', 'recruiter','admin']

class UserSchema(SQLAlchemySchema):
    class Meta:
        model = UserModel
        load_instance = True  #gives you a JobModel instance
    
    id = auto_field(dump_only=True)
    name = auto_field(required=True)
    email = auto_field(required=True)
    password = auto_field(required=True)  
    role = auto_field(required=True)
    created_at = auto_field(dump_only=True)
    status = auto_field(dump_only =True)
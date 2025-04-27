from marshmallow import Schema, fields, validates, ValidationError
from marshmallow.validate import Length, Email
from app.models import UserModel
import re

VALID_ROLES = ['job_seeker', 'recruiter']

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str(required=True, validate=Email())
    password = fields.Str(required=True, validate=Length(min=6))
    name = fields.Str(required=True, validate=Length(min=1))
    created_at = fields.DateTime(dump_only=True)
    role = fields.Str(default='job_seeker', validate=lambda x: x in VALID_ROLES)

    @validates('email')
    def validate_email(self, value):
        # Add custom email validation logic if needed
        if UserModel.query.filter_by(email=value).first():
            raise ValidationError("Email already exists")
    
    @validates('password')
    def validate_password(self,value):
        if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).{6,}$', value):
            raise ValidationError("Password must contain at least one uppercase letter, one lowercase letter, one number, and be at least 6 characters long")

    @validates('role')
    def validate_role(self, value):
        if value not in VALID_ROLES:
            raise ValidationError(f"Invalid role. Valid roles are: {', '.join(VALID_ROLES)}")
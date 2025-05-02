from marshmallow import Schema, fields, validates, ValidationError
from marshmallow.validate import Length, Email

import re

VALID_ROLES = ['candidate', 'recruiter','admin']

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str(required=True, validate= Email())
    password = fields.Str(required=True, validate=Length(min=6))
    name = fields.Str(required=True, validate=Length(min=3))
    created_at = fields.DateTime(dump_only=True)
    role = fields.Str(required=True, validate=lambda x: x in VALID_ROLES) 

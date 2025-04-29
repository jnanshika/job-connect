from marshmallow import Schema, fields, validate
from marshmallow.validate import Length

class JobSchema(Schema):
    id = fields.Int(dump_only= True)
    title = fields.Str(required= True, validate = Length(min=5))
    description = fields.Str(required= True, validate = Length(min=5))
    posted_by = fields.Int(required= True)
    created_at = fields.DateTime(dump_only= True)
    location = fields.Str(required= True, validate = Length(min=3))
        
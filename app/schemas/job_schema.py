from marshmallow import Schema, fields, validate
from marshmallow.validate import Length

Valid_JobStatus = ['Active' , 'Inactive']

class JobSchema(Schema):

    # load_instance = True   # 🔥 makes load() return model instance
    # include_fk = True      # 🔥 allows foreign key like posted_by


    id = fields.Int(dump_only= True)
    title = fields.Str(required= True, validate = Length(min=5))
    description = fields.Str(required= True, validate = Length(min=5))
    posted_by = fields.Int(required= True)
    created_at = fields.DateTime(dump_only= True)
    location = fields.Str(required= True, validate = Length(min=3))
    status = fields.Str(required= True, validate= lambda x:x in Valid_JobStatus) 
        
from app.extensions import db
from datetime import datetime, timezone

class JobModel(db.Model):
    __tablename__ = "jobs"

    #define columns
    id = db.Column(db.Integer, primary_key =True  ,nullable = False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    posted_by = db.Column(db.Integer, db.ForeignKey('users.id') , nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    location = db.Column(db.String(100), nullable=False)
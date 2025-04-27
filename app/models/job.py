from app.extensions import db
from datetime import datetime, timezone

class JobModel(db.Model):
    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    location = db.Column(db.String(100), nullable = False)
    posted_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False )
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

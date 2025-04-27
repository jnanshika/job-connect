from app.extensions import db
from datetime import datetime, timezone
from enum import Enum

class ApplicationStatus(Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    INPROGRESS = "inprogress"

class ApplicationModel:
    __table__ = "ApplicationModel"

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('UserModel.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('JobModel.id'), nullable=False)
    status = db.Column(db.Enum(ApplicationStatus), default=ApplicationStatus.PENDING)
    applied_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

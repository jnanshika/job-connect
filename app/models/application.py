from datetime import datetime, timezone
from app.extensions import db
from sqlalchemy.orm import relationship

Valid_ApplicationStatus = ['Applied', 'Inprogress', 'Denied', 'Hired', 'Inactive']

class ApplicationModel(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(50), default='Applied', nullable=False)  # applied, in_progress, hired, rejected, inactive
    resume = db.Column(db.String(255), nullable=True)  # URL/path to the uploaded resume
    applied_on = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    job = relationship("JobModel", back_populates="applications")
    user = relationship("UserModel", back_populates="applications")

    __table_args__ = (
        db.UniqueConstraint('job_id', 'user_id', name='unique_application'),
    )

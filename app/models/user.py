from app.extensions import db
from datetime import datetime, timezone

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key =True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    #We use a lambda so that it’s called fresh whenever a row is inserted (not evaluated once at server start).
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    role = db.Column(db.String(20), nullable=False)
    # ✅ Add the new column
    status = db.Column(db.String(10), nullable=True, default='active') 
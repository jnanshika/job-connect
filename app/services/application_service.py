from app.extensions import db
from flask import request, jsonify
from sqlalchemy.exc import IntegrityError

class ApplicationService:
    @staticmethod
    def create_application(application):
        try: 
            db.session.add(application)
            db.session.commit()
            return {"message": "Application submitted successfully"}, 201
        except IntegrityError as e:
            db.session.rollback()
            # Check for unique constraint failure
            if "unique_application" in str(e.orig):
                return jsonify({"error": "You have already applied to this job."}), 409
            return jsonify({"error": "Database integrity error."}), 500

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
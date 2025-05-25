from app.models import UserModel, JobModel, ApplicationModel
from bcrypt import hashpw, checkpw, gensalt
from app.extensions import db
from datetime import timedelta
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

class AuthService:
    @staticmethod
    def register_user(user):
        # Check if user already exists
        existing_user = UserModel.query.filter_by(email=user.email).first()
        if existing_user:
            return {"message": "An account already exists with this email!"}, 400
        
        hashed_password = hashpw(user.password.encode(), gensalt()).decode('utf-8')
        user.password = hashed_password
        try: 
            db.session.add(user) 
            db.session.commit()
        except:
            db.session.rollback()
            return {"error" : "Error occured while email registration"} , 400

        return {"message": "Email registered successfully"}, 201
    
    @staticmethod
    def login_user(user):
        db_user = UserModel.query.filter_by(email=user.email).first()
        if not db_user : 
            return {"error": "User not found!"}, 404
        
        #checkpw(plain password(user enter), encrypted password (database hashed password))
        if not checkpw(user.password.encode('utf-8'), db_user.password.encode('utf-8')):
            return {"error": "Incorrect password!"}, 401
        
        # Create access token
        access_token = create_access_token(identity=str(db_user.id), expires_delta=timedelta(hours=1))
        return {"access_token": access_token}, 200

    def deactivate_user(user_id : int):
        try:
            user = UserModel.query.filter_by(id = user_id).first()
            user.status = 'inactive'
            # Check the user's role
            if user.role == 'candidate':
                # Deactivate all applications associated with this candidate
                for application in user.applications:
                    application.status = 'Inactive'
            
            elif user.role == 'recruiter':
                # Deactivate all job postings associated with this recruiter
                user_job_postings = JobModel.query.filter_by(posted_by = user.id).all()
                for job_posting in user_job_postings:
                    job_posting.status = 'Inactive'

            db.session.commit()
            return {"message": f"User with ID {user.id} was marked inactive"}, 200
        
        except Exception as e:
            db.session.rollback()
            return {"error": f"Error while marking user as inactive. {str(e)}"}, 400
        
    # def delete_user(user_id):
    #     user = UserModel.query.filter_by(id = user_id).first()
    #     db.session.delete(user)
    #     db.session.commit()

    #     return {"message" : "User deleted succesfully"}, 200
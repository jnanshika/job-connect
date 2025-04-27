from app.models import UserModel
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from flask_jwt_extended import create_access_token, decode_token
from datetime import timedelta

class AuthService:
    @staticmethod
    def register_user(email, password, name, role='job_seeker'):
        # Check if user already exists
        existing_user = UserModel.query.filter_by(email=email).first()
        if existing_user:
            return {"message": "User already exists!"}, 400
        
        #hashed_password = generate_password_hash(password, method='sha256')
        new_user = UserModel(email=email, password=password, name=name, role=role)
        db.session.add(new_user)
        db.session.commit()

        return {"message": "User registered successfully!"}, 201
    
    @staticmethod
    def login_user(email, password):
        user = UserModel.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return {"message": "Invalid credentials!"}, 401
        
        # Create access token
        access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=1))
        return {"access_token": access_token}, 200

    @staticmethod
    def verify_token(token):
        try:
            decoded_token = decode_token(token)
            return decoded_token
        except Exception as e:
            return {"message": f"Invalid token! {str(e)}"}, 400

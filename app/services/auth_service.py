from app.models import UserModel
from bcrypt import hashpw, checkpw, gensalt
from app.extensions import db, jwt
from datetime import timedelta
from flask_jwt_extended import get_jwt_identity, jwt_required, create_access_token,decode_token

class AuthService:
    @staticmethod
    def register_user(email, password, name, role):
        # Check if user already exists
        existing_user = UserModel.query.filter_by(email=email).first()
        if existing_user:
            return {"message": "User already exists!"}, 400
        
        hashed_password = hashpw(password.encode(), gensalt()).decode('utf-8')
        new_user = UserModel(email=email, password=hashed_password, name=name, role=role)
        db.session.add(new_user) 
        db.session.commit()

        return {"message": "User registered successfully!"}, 201
    
    @staticmethod
    def login_user(email, password):
        user = UserModel.query.filter_by(email=email).first()
        if not user : 
            return {"message": "User not found!"}, 404
        
        if not checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return {"message": "Incorrect password!"}, 401
        
        # Create access token
        access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(hours=1))
        return {"access_token": access_token}, 200

    @staticmethod
    def verify_token(token):
        try:
            decoded_token = decode_token(token)
            return decoded_token
        except Exception as e:
            return {"message": f"Invalid token! {str(e)}"}, 400
        
    @jwt_required()
    def authorise_token():
        current_userid = get_jwt_identity()
        if current_userid:
            return {"message": f"Authorised user: {current_userid}"}, 202
        
        return {"message": "UnAuthorised"}, 401
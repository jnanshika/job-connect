from functools import wraps
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask import jsonify
from app.models import UserModel  

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            if not user_id:
                return jsonify({"error": "Unauthorized user"}), 401
            user = UserModel.query.get(user_id)
            if not user:
                return jsonify({"error": f"No user is registered with {user.email}"}), 404
            return f(user, *args, **kwargs)
        
        except Exception as e:
            return jsonify({"error": str(e)}), 401
    return decorated_function

def recruiter_required(f):
    @wraps(f)
    @token_required
    #the token_required function returns a user
    def decorated_function(user, *args, **kwargs):
        if not user or user.role != "recruiter":
            return {"error": f"User must be a recruiter {user}"}, 403
        return f(user, *args, **kwargs)
    return decorated_function

def candidate_required(f):
    @wraps(f)
    @token_required
    #the token_required function returns a user
    def decorated_function(user, *args, **kwargs):
        if not user or user.role != "candidate":
            return jsonify({"error": "Only candidates can perform this action"}), 403
        return f(user, *args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    @token_required
    def decorated_function(user_id,*args, **kwargs):
        user = UserModel.query.get(user_id)
        if not user or user.role != "admin":
            return jsonify({"error": "Only admin can perform this action"}), 403
        return f(user, *args, **kwargs)
    return decorated_function
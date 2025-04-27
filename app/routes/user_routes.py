from flask import Blueprint, request
from app.services.auth_service import AuthService

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    
    if not email or not password or not name:
        return {"message": "Missing required fields!"}, 400

    return AuthService.register_user(email, password, name)

@user_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return {"message": "Missing required fields!"}, 400

    return AuthService.login_user(email, password)

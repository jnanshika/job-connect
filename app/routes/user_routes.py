from flask import Blueprint, jsonify, request
from app.services import AuthService
from app.models import UserModel
from app.schemas import VALID_ROLES, ValidationError, UserSchema
#from app.extensions import jwt

#Blueprint = a way to group related routes together cleanly.
user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/register', methods=['POST'])
def register():
    jsondata = request.get_json()

    #deserialise the data
    try:
        user_schema = UserSchema()
        user_object = user_schema.load(jsondata)
    
    except ValidationError as error:
        return {"errors": error.messages}, 400
    
    if user_object['role'] not in VALID_ROLES:
        return jsonify({"error": "Invalid role provided"}), 400
    
    return AuthService.register_user(user_object['email'], user_object['password'] , user_object['name'] , user_object['role'] )

@user_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return {"message": "Missing required fields!"}, 400

    return AuthService.login_user(email, password)

@user_routes.route('/allusers', methods=['GET'])
def get_all_users():
    users = UserModel.query.all()  # Get all user records from database - Python object
    
    schema = UserSchema(many=True) #many helps to check for more than one record

    return {"users": schema.dump(users)}, 200


@user_routes.route('/login/id', methods=['GET'])
def secure_login():
    return AuthService.authorise_token()
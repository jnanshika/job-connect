from flask import Blueprint, jsonify, request
from app.services import AuthService
from app.models import UserModel
from app.schemas import VALID_ROLES, ValidationError, UserSchema
from app.extensions import db
from app.utils import admin_required, token_required

#Blueprint = a way to group related routes together cleanly.
user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/register', methods=['POST'])
def register():
    jsondata = request.get_json()

    try:
        user_schema = UserSchema(session =db.session)
        user = user_schema.load(jsondata)  #Deserialisation
    
    except ValidationError as error:
        return {"errors": error.messages}, 400
    
    if user.role not in VALID_ROLES:
        return jsonify({"error": "Invalid role provided"}), 400
    
    return AuthService.register_user(user)

@user_routes.route('/login', methods=['POST'])
def login():
    jsondata = request.get_json()
    email = jsondata.get('email')
    password = jsondata.get('password')

    if not email or not password:
        return {"error": "Email and password are required and cannot be empty."}, 400

    try:
        user_schema = UserSchema(session =db.session)
        user = user_schema.load(jsondata, partial =True)  #Deserialisation
    except ValidationError as error:
        return {"errors": error.messages}, 400
    
    return AuthService.login_user(user)

@user_routes.route('/', methods=['GET'])
def get_all_users():
    users = UserModel.query.all()  # Get all user records from database - Python object
    
    schema = UserSchema(many=True) #many helps to check for more than one record

    return {"users": schema.dump(users)}, 200

@user_routes.route('/<int:user_id>/deactivate', methods = ['PATCH'])
@token_required
def deactivate_user(loggeduser, user_id):
    if loggeduser.role!= 'admin' and loggeduser.id != user_id:
        return {"error": f"{loggeduser.name} is not authorized to deactivate this user"}, 403
    return AuthService.deactivate_user(user_id)

# #Only for testing - should be update to admin only or automate to delete deactivate accounts >30 days
# @user_routes.route('/<int:user_id>/delete', methods= ['DELETE'])
# @admin_required
# def delete_user(user, user_id):
#     return AuthService.delete_user(user_id)
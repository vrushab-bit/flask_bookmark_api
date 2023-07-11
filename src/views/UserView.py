from flask import request, json, Response, Blueprint,g
from marshmallow import ValidationError
from ..models.UserModel import UserModel, UserSchema
from ..shared.Authentication import Auth

user_api = Blueprint('users', __name__)
user_schema = UserSchema()


# Unauthorized Endpoints

@user_api.route('/', methods=['POST'])
def create():
    """
    Create User Function
    """

    try:
        req_data = request.get_json()
        data= user_schema.load(req_data)
    except ValidationError as err:
        return custom_response({'error': "Incorrect Data Format"}, 400)

    # Check if the user exists
    user_in_db = UserModel.get_user_by_email(data.get('email'))
    if user_in_db:
        message = {'error': 'User already exists'}
        return custom_response(message, 400)
    
    user = UserModel(data)
    user.save()

    ser_data = user_schema.dump(user)
    print(ser_data.get('id'))
    token = Auth.generate_token(ser_data.get('id'))
    
        
    return custom_response({'jwt_token': token}, 201)



@user_api.route('/', methods=['GET'])
@Auth.auth_required
def get_all():
    """
	Get All Users
	"""
    users = UserModel.get_all_users()
    ser_users = user_schema.dump(users, many=True)
    
    return custom_response(ser_users, 200)



@user_api.route('/<int:user_id>', methods=['GET'])
@Auth.auth_required
def get_a_user(user_id):
    """
	Get A Single User
	"""
    user = UserModel.get_one_user(user_id)
    if not user:
        return custom_response({'error': 'user not found'}, 404)
    ser_user = user_schema.dump(user)
    return custom_response(ser_user, 200)



@user_api.route('/me', methods=['PUT'])
@Auth.auth_required
def update():
    """
    Update Me
    """
    try:
        req_data = request.get_json()
        data= user_schema.load(req_data, partial=True)
    except ValidationError as err:
        return custom_response({'error': "Incorrect Data Format"}, 400)
    
    user = UserModel.get_one_user(g.user.get('id'))
    user.update(data)
    ser_user = user_schema.dump(user)
    return custom_response(ser_user, 200)



@user_api.route('/me', methods=['DELETE'])
@Auth.auth_required
def delete():
    """
    Delete A User
    """
    user = UserModel.get_one_user(g.user.get('id'))
    user.delete()
    return custom_response({'message': 'deleted'}, 204)



@user_api.route('/me', methods=['GET'])
@Auth.auth_required
def get_me():  
    """
    Get Me
    """
    user = UserModel.get_one_user(g.user.get('id'))
    ser_user = user_schema.dump(user)
    return custom_response(ser_user, 200)




@user_api.route('/login', methods=['POST'])
def login():
    """
    User Login Function
    """
    try:
        req_data = request.get_json()
        data= user_schema.load(req_data, partial=True)
    except ValidationError as err:
        return custom_response({'error': "Incorrect Data Format"}, 400)
    
    if not data.get('email') or not data.get('password'):
        return custom_response({'error': 'You need Email And Password To Sign In'}, 400)
    
    user = UserModel.get_user_by_email(data.get('email'))
    

    if not user:
        return custom_response({'error': 'invalid creds'}, 400)
    if not user.check_hash(data.get('password')):
        return custom_response({'error': 'invalid creds'}, 400)
    
    ser_data = user_schema.dump(user)
    token = Auth.generate_token(ser_data.get('id'))

    return custom_response({'jwt_token': token}, 200)




    



# Utility Functions
def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )

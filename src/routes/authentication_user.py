from flask import Blueprint, request, jsonify
from utils.jwt import write_token, validate_token
from services.users import new_user, validate_user

bp = Blueprint('authentication_user', __name__, url_prefix='/api/v1/auth_user')

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    token = data.get('token')

    user_exists = validate_user(username, password)
    
    token_validation = validate_token(token, output=True)
    
    if user_exists.message == "User authenticated" and token_validation.message != "Token invalid":
        if token_validation.message == "Token expired":
            data = {
                "username": username,
                "password": password
            }
            token = write_token(data)
        return token_validation, 200
    
    if user_exists.message != "User authenticated":
        return jsonify({"message User": user_exists.message}), user_exists.status_code
    
    if token_validation.message == "Token invalid":
        return jsonify({"message Token": token_validation.message}), token_validation.status_code

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    new_user_response = new_user(username, password)
    
    return jsonify({"message": new_user_response.message}), new_user_response.status_code

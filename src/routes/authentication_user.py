from flask import Blueprint, request, jsonify
from src.utils.jwt import write_token, validate_token
from src.services.users import new_user, validate_user
from src.models.user_model import User
from src.databases.conection import db

bp = Blueprint('authentication_user', __name__, url_prefix='/api/v1/auth_user')

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user_exists_response = validate_user(username, password)
    token = user_exists_response["token"]
    token_validation_response = validate_token(token, output=True)
    token_message = token_validation_response["message"]

    if user_exists_response["message"] == "User authenticated" and token_message != "Token invalid":
        print("User authenticated")
        if token_message == "Token expired":
            new_data = {
                "username": username,
                "password": password
            }
            token = write_token(new_data)
            user = User.query.filter_by(username=username).first()
            user.token = token  
            db.session.commit()
        return jsonify(token_message), 200

    if user_exists_response["message"] == "User not found":
        return jsonify({"message User": user_exists_response["message"]}), 404
    
    if user_exists_response["message"] == "Invalid password":
        return jsonify({"message User": user_exists_response["message"]}), 401

    if token_message == "Token invalid":
        return jsonify({"message Token": token_message}), 401

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    new_user_response, new_user_status = new_user(username, password)
    return jsonify({"message": new_user_response["message"]}), new_user_status
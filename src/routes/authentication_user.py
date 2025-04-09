from flask import Blueprint, request, jsonify
from src.utils.jwt import write_token, validate_token
from src.services.users import new_user, validate_user

bp = Blueprint('authentication_user', __name__, url_prefix='/api/v1/auth_user')

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user_exists_response, user_exists_status = validate_user(username, password)
    token = user_exists_response["token"] if user_exists_status == 200 else None
    token_validation_response, token_validation_status = validate_token(token, output=True)
    token_message = token_validation_response["message"]
    print(user_exists_response)
    print(user_exists_status)
    print(token)
    print(token_validation_response)
    print(token_message)
    print(token_validation_status)

    if user_exists_response["message"] == "User authenticated" and token_message != "Token invalid":
        print("User authenticated")
        if token_message == "Token expired":
            new_data = {
                "username": username,
                "password": password
            }
            token = write_token(new_data)
        return jsonify(token_message), 200

    if user_exists_response["message"] != "User authenticated":
        return jsonify({"message User": user_exists_response["message"]}), user_exists_status

    if token_message == "Token invalid":
        return jsonify({"message Token": token_message}), token_validation_status

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    new_user_response, new_user_status = new_user(username, password)
    return jsonify({"message": new_user_response["message"]}), new_user_status
from models.user_model import UserModel
from werkzeug.security import generate_password_hash, check_password_hash
from utils.jwt import write_token, validate_token
from flask import jsonify
from src import db


def new_user(username, password):
    
    user_exists = UserModel.query.filter_by(username=username).first()
    if user_exists:
        return {"message": "User already exists"}, 409
    
    data = {
        "username": username,
        "password": password
    }
    token = write_token(data)
    
    user = UserModel(username=username, password=generate_password_hash(password), token=token)
    
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        return {"message": "Error creating user"}, 500
    
def validate_user(username, password):
    
    user = UserModel.query.filter_by(username=username).first()
    
    if not user:
        return {"message": "User not found"}, 404
    
    if not check_password_hash(user.password, password):
        return {"message": "Invalid password"}, 401
    
    return {"message": "User authenticated"}, 200
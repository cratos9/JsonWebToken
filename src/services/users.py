from src.models.user_model import User
from werkzeug.security import generate_password_hash, check_password_hash
from src.utils.jwt import write_token
from src import db


def new_user(username, password):
    
    user_exists = User.query.filter_by(username=username).first()
    if user_exists:
        return {"message": "User already exists"}, 409
    
    data = {
        "username": username,
        "password": password
    }
    token = write_token(data)
    
    user = User(username=username, password=generate_password_hash(password), token=token)
    
    try:
        db.session.add(user)
        db.session.commit()
        return {"message": "User created successfully"}, 201
    except Exception as e:
        return {"message": "Error creating user"}, 500
    
def validate_user(username, password):
    
    user = User.query.filter_by(username=username).first()
    
    if not user:
        return {"message": "User not found"}
    
    if not check_password_hash(user.password, password):
        return {"message": "Invalid password"}
    
    return {"message": "User authenticated", "token": user.token }
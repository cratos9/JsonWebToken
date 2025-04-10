import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from flask import jsonify
from jwt import encode, decode, exceptions

load_dotenv()

def expired_token(days):
    now = datetime.now()
    new_time = now + timedelta(days)
    return new_time

def write_token(data):
    token = encode(
        payload={**data, "exp": expired_token(1)},
        key=os.getenv("SECRET_KEY"),
        algorithm="HS256"
    )
    return token.encode('utf-8')

def validate_token(token, output=False):
    try:
        decoded = decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
        if output:
            return {"message": "Token valid", "decoded": decoded}
        return {"message": "Token valid"}
    except exceptions.ExpiredSignatureError:
        return {"message": "Token expired"}
    except exceptions.DecodeError:
        return {"message": "Token invalid"}
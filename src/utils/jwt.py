from jwt import encode, decode, exceptions
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from flask import jsonify

load_dotenv()

def expired_token(days):
    now = datetime.now()
    new_time = now + timedelta(days)
    return new_time

def write_token(data):
    token = encode(playload={**data, "exp":expired_token(1)}, key = os.getenv("SECRET_KEY"), algorithm="HS256")
    return token.encode("utf-8")

def validate_token(token, output=False):
    try:
        if output:
            return decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
    except exceptions.ExpiredSignatureError:
        return jsonify({"message":"Token expired"}), 401
    except exceptions.DecodeError:
        return jsonify({"message":"Token invalid"}), 401
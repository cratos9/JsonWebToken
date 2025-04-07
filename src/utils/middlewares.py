from routes.index import bp as index_bp
from flask import request
from jwt import validate_token

@index_bp.before_request
def verify_token_middleware():
    token = request.headers.get('Authorization').split(" ")[1]
    validate_token(token, output=False)
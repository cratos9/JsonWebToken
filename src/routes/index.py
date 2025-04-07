from flask import Blueprint, request, jsonify

bp = Blueprint('index', __name__, url_prefix='/api/v1')

@bp.route('/', methods=['POST'])
def index():
    data = request.get_json()
    username = data.get('username')
    return jsonify({"message": f"Hello {username}"}), 200
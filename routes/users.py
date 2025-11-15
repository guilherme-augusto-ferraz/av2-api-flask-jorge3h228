from flask import Blueprint, request, jsonify, abort
from database import db
from models.user import User

users_bp = Blueprint('users', __name__, url_prefix='/users')


@users_bp.route('/', methods=['GET'])
def list_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])


@users_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    username = data.get('username')
    email = data.get('email')
    if not username or not email:
        return jsonify({'error': 'username and email are required'}), 400

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({'error': 'user with same username or email exists'}), 400

    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

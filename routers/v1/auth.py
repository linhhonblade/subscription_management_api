import os

from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from datetime import datetime, timedelta
import jwt
from models import db, users
from passlib.hash import bcrypt

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hash_pwd = bcrypt.hash(data.get('password'))
    user = users.User(
        name = data.get('name'),
        email = data.get('email'),
        password = hash_pwd
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({
        'message': 'User registered successfully',
        'user_id': user.id
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({
            'message': 'Missing email or password',
        }), 401

    # Check if user exists
    user = users.User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({
            'message': 'Invalid email or password',
        }), 401

    # Generate JWT token
    access_token = jwt.encode({
        "user_id": user.id,
        "exp": datetime.utcnow() + timedelta(seconds=os.getenv('JWT_ACCESS_EXPIRATION_SECONDS', 3600))
    }, os.getenv('JWT_SECRET_KEY'), algorithm="HS256")

    refresh_token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(seconds=os.getenv('JWT_REFRESH_EXPIRATION_SECONDS', 604800))  # 7 days
    }, os.getenv('JWT_SECRET_KEY'), algorithm="HS256")

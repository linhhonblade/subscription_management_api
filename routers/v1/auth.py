from flask import Blueprint, request, jsonify
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
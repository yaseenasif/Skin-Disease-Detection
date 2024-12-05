from flask import Blueprint, request, jsonify
from app.models import User, Profile
from app.extensions import db

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register_user():
    data = request.json
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    if not (email and username and password):
        return jsonify({'error': 'Missing data'}), 400

    new_user = User(email=email, username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully!'}), 201

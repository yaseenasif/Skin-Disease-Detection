import bcrypt
from flask import Blueprint, request, jsonify
from app.models import User
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

    validation_result = validate_new_user(email=email, username=username, password=password)
    if validation_result is not None:
        return validation_result
        
    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Create a new user instance
    new_user = User(email=email, username=username, password=hashed_password.decode('utf-8'))
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully!'}), 201


def validate_new_user(email,username,password):
    if not is_valid_email(email):
        return jsonify({"error": "Email is not valid"}), 400
    
    if not is_valid_password(password):
        return jsonify({"error": "Password is not valid"}), 400
        
    existing_user_by_email = User.query.filter_by(email=email).first()
    if existing_user_by_email:
        return jsonify({"error": "An account is already exist with this Email, please try with another one."}), 400

    existing_user_by_username = User.query.filter_by(username=username).first()
    if existing_user_by_username:
        return jsonify({"error": "That username already exists. Please choose a different one."}), 400


def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    match = re.match(pattern, email)
    return bool(match)

def is_valid_password(password):
    if len(password) < 8:
        return False
    
    if not any(char.isupper() for char in password):
        return False
    
    if not any(char.islower() for char in password):
        return False
    
    if not any(char.isdigit() for char in password):
        return False
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    
    return True


@auth_bp.route('/login', methods=['POST'])
def signin_user():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user = User.query.filter_by(username=username).first()
    
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid username or password'}), 401
    # login_user(user=user, remember=True)
    return jsonify({'message': 'SignIn successful'}), 200
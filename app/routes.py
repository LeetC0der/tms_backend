from flask import Blueprint, request, jsonify
from .helper_functions.password_validator import validate
from flask_jwt_extended import create_access_token, get_jwt_identity, create_refresh_token, jwt_required
from flask_jwt_extended.exceptions import JWTDecodeError
from werkzeug.exceptions import Unauthorized
from .models import User, db
import datetime
main = Blueprint('main', __name__)

@main.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':    
        req_json = request.get_json()
        if not req_json:
            return jsonify({'message': 'Invalid input'}), 400
        email = req_json.get('email')
        password = req_json.get('password')
        if not email:
            return jsonify({'message': 'email is a required field'}), 400
        if not password:
            return jsonify({'message': 'password is a required field'}), 400
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            access_token = create_access_token(identity=user.username, expires_delta=datetime.timedelta(minutes=15))
            refresh_token = create_refresh_token(identity=user.username, expires_delta=datetime.timedelta(days=30))
            user_info = {
                'id': user.id,
                'email': user.email,
                'username': user.username,
            }
            return jsonify(access_token=access_token, refresh_token=refresh_token,userInfo=user_info), 200
        else:
            return jsonify({'message': 'Invalid email or password'}), 401

@main.route('/signUp', methods=['POST'])
def sign_up():
    try:
        req_json = request.get_json()
        email = req_json['email']
        username = req_json['username']
        password = req_json['password']
        if User.query.filter_by(email=email).first():
            return jsonify({"message": f"Email: {email} already exists, please try a different email."}), 409
        if User.query.filter_by(username=username).first():
            return jsonify({"message": f"Username: {username} already exists, please try a different username."}), 409
        validation_result = validate(password)
        if validation_result != 'Valid':
            return jsonify({'password': validation_result}), 400
        # Create a new user with email, username, and password
        new_user = User(email=email, username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'success': 'User created successfully'}), 201
    except Exception as error:
        return jsonify({'error': str(error)}), 500

@main.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    try:
        # Your logic to create a new access token using the refresh token
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)
        return jsonify(access_token=new_access_token), 200
    except JWTDecodeError as e:
        return jsonify({"msg": "Error decoding token", "error": str(e)}), 401
    except Unauthorized as e:
        return jsonify({"msg": "Incorrect or expired refresh token", "error": str(e)}), 401
    except Exception as e:
        return jsonify({"msg": "An error occurred", "error": str(e)}), 500

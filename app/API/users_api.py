# app/API/users_api.py

from flask import Blueprint, jsonify, request, abort
from app.models import User, Apartment
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db, bcrypt

users_api_bp = Blueprint('users_api', __name__, url_prefix='/api')


def serialize_user(user):
    return {
        'UserId': user.UserID,
        'Email': user.Email,
        'IsStudent': user.IsStudent,
        'Name': user.Name,
        'PhoneNumber': user.PhoneNumber,
        'UserType': user.UserType,
        'RegistrationDate': user.RegistrationDate,
        'UserImage': user.UserImage
    }


@users_api_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    return jsonify([serialize_user(user) for user in users]), 200


@users_api_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(serialize_user(user)), 200


@users_api_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('Email')
    password = data.get('Password')

    user = User.query.filter_by(Email=email).first()
    if user and bcrypt.check_password_hash(user.Password, password):
        if user.UserType != 'admin':
            return jsonify({"msg": "Access denied: admin only"}), 403
        access_token = create_access_token(identity={'email': user.Email})
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Invalid email or password"}), 401


@users_api_bp.route('/users', methods=['POST'])
@jwt_required()
def create_user():
    data = request.json
    if User.query.filter_by(Email=data['Email']).first():
        return jsonify({'message': 'User with this email already exists'}), 409
    new_user = User(
        Email=data['Email'],
        Password=data['Password'],
        IsStudent=data['IsStudent'],
        Name=data['Name'],
        PhoneNumber=data.get('PhoneNumber', None),
        UserType=data['UserType'],
        UserImage=data.get('UserImage', None)
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully', 'UserID': new_user.UserID}), 201


@users_api_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json
    if get_jwt_identity() != user.UserID:
        return jsonify({'message': 'Permission denied'}), 403

    user.Email = data.get('Email', user.Email)
    user.Password = data.get('Password', user.Password)
    user.IsStudent = data.get('IsStudent', user.IsStudent)
    user.Name = data.get('Name', user.Name)
    user.PhoneNumber = data.get('PhoneNumber', user.PhoneNumber)
    user.UserType = data.get('UserType', user.UserType)
    user.UserImage = data.get('UserImage', None)

    db.session.commit()
    return jsonify({'message': 'User updated successfully', 'UserID': user.UserID}), 200


@users_api_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if get_jwt_identity() != user.UserID:
        return jsonify({'message': 'Permission denied'}), 403
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully', 'UserID': user.UserID}), 200

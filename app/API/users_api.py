# app/API/users_api.py

from flask import Blueprint, jsonify, request, abort
from app.models import User, Apartment
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
def get_users():
    users = User.query.all()
    return jsonify([serialize_user(user) for user in users]), 200


@users_api_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    print(user.check_password('password123'))
    return jsonify(serialize_user(user)), 200


@users_api_bp.route('/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(
        Email=data['Email'],
        Password=data['Password'],
        IsStudent=data['IsStudent'],
        Name=data['Name'],
        PhoneNumber=data['PhoneNumber'],
        UserType=data['UserType'],
        UserImage=data.get('UserImage', None)
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully', 'UserID': new_user.UserID}), 201


@users_api_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json

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
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully', 'UserID': user.UserID}), 200

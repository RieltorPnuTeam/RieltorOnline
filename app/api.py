# app/api.py

from flask import Blueprint, jsonify, request, abort
from app.models import User, Apartment
from app import db

api_bp = Blueprint('api', __name__, url_prefix='/api')


def serialize_user(user):
    return {
        'UserId': user.UserID,
        'Email': user.Email,
        'IsStudent': user.IsStudent,
        'Name': user.Name,
        'PhoneNumber': user.PhoneNumber,
        'UserType': user.UserType,
        'RegistrationDate': user.RegistrationDate
    }


@api_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([serialize_user(user) for user in users]), 200


@api_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(serialize_user(user)), 200
# app/API/roommates_api.py

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.models import Roommate
from app import db

roommates_api_bp = Blueprint('roommates_api', __name__, url_prefix='/api')


def serialize_roommate(roommate):
    return {
        'RoommateID': roommate.RoommateID,
        'UserID': roommate.UserID,
        'ApartmentID': roommate.ApartmentID
    }


@roommates_api_bp.route('/roommates', methods=['GET'])
@jwt_required()
def get_roommates():
    roommates = Roommate.query.all()
    return jsonify([serialize_roommate(roommate) for roommate in roommates]), 200


@roommates_api_bp.route('/roommates/<int:roommate_id>', methods=['GET'])
@jwt_required()
def get_roommate(roommate_id):
    roommate = Roommate.query.get_or_404(roommate_id)
    return jsonify(serialize_roommate(roommate)), 200


@roommates_api_bp.route('/roommates', methods=['POST'])
@jwt_required()
def create_roommate():
    data = request.get_json()
    new_roommate = Roommate(
        UserID=data['UserID'],
        ApartmentID=data['ApartmentID']
    )
    db.session.add(new_roommate)
    db.session.commit()
    return jsonify({'message': 'Roommate created', 'RoommateID': new_roommate.RoommateID}), 201


@roommates_api_bp.route('/roommates/<int:roommate_id>', methods=['DELETE'])
@jwt_required()
def delete_roommate(roommate_id):
    roommate = Roommate.query.get_or_404(roommate_id)
    db.session.delete(roommate)
    db.session.commit()
    return jsonify({'message': 'Roommate deleted'}), 200

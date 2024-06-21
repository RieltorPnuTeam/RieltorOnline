# app/API/favorites_api.py

from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import jwt_required
from app.models import Favorite, User, Apartment
from app import db

favorites_api_bp = Blueprint('favorites_api', __name__, url_prefix='/api')


def serialize_favorite(favorite):
    return {
        'FavoriteID': favorite.FavoriteID,
        'UserID': favorite.UserID,
        'ApartmentID': favorite.ApartmentID
    }


@favorites_api_bp.route('/favorites', methods=['GET'])
@jwt_required()
def get_favorites():
    favorites = Favorite.query.all()
    return jsonify([serialize_favorite(favorite) for favorite in favorites]), 200


@favorites_api_bp.route('/favorites/<int:favorite_id>', methods=['GET'])
@jwt_required()
def get_favorite(favorite_id):
    favorite = Favorite.query.get_or_404(favorite_id)
    return jsonify(serialize_favorite(favorite)), 200


@favorites_api_bp.route('/favorites', methods=['POST'])
@jwt_required()
def create_favorite():
    data = request.get_json()

    user_id = data.get('UserID')
    apartment_id = data.get('ApartmentID')

    new_favorite = Favorite(
        UserID=user_id,
        ApartmentID=apartment_id
    )

    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({'message': 'Favorite created', 'FavoriteID': new_favorite.FavoriteID}), 201


@favorites_api_bp.route('/favorites/<int:favorite_id>', methods=['DELETE'])
@jwt_required()
def delete_favorite(favorite_id):
    favorite = Favorite.query.get_or_404(favorite_id)
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({'message': 'Favorite deleted'}), 200

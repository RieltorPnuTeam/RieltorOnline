# app/API/apartment_images_api.py

from flask import Blueprint, jsonify, request, abort
from app.models import ApartmentImage
from app import db

apartment_images_api_bp = Blueprint('apartment_images_api', __name__, url_prefix='/api')


def serialize_apartment_image(image):
    return {
        'ImageID': image.ImageID,
        'ApartmentID': image.ApartmentID,
        'ImageURL': image.ImageURL
    }


@apartment_images_api_bp.route('/apartment_images', methods=['POST'])
def create_apartment_image():
    data = request.get_json()
    new_image = ApartmentImage(
        ApartmentID=data['ApartmentId'],
        ImageURL=data['ImageURL']
    )
    db.session.add(new_image)
    db.session.commit()
    return jsonify({'message': 'Image added', 'ImageID': new_image.ImageID}), 201


@apartment_images_api_bp.route('/apartment_images/<int:image_id>', methods=['PUT'])
def update_apartment_image(image_id):
    data = request.get_json()
    image = ApartmentImage.query.get_or_404(image_id)
    image.ImageURL = data.get('ImageURL', image.ImageURL)
    db.session.commit()
    return jsonify({'message': 'Image updated'}), 200


@apartment_images_api_bp.route('/apartment_images/<int:image_id>', methods=['DELETE'])
def delete_apartment_image(image_id):
    image = ApartmentImage.query.get_or_404(image_id)
    db.session.delete(image)
    db.session.commit()
    return jsonify({'message': 'Image deleted'}), 200


@apartment_images_api_bp.route('/apartment_images/<int:apartment_id>', methods=['GET'])
def get_apartment_images(apartment_id):
    images = ApartmentImage.query.filter_by(ApartmentID=apartment_id).all()
    return jsonify([serialize_apartment_image(image) for image in images]), 200

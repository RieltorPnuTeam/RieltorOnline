# app/apartments_api.py

from flask import Blueprint, jsonify, request, abort
from app.models import User, Apartment
from app import db

apartments_api_bp = Blueprint('apartments_api', __name__, url_prefix='/api')


def serialize_apartment(apartment):
    return {
        'ApartmentId': apartment.ApartmentId,
        'OwnerId': apartment.OwnerId,
        'Type': apartment.Type,
        'City': apartment.City,
        'Street': apartment.Street,
        'HouseNum': apartment.HouseNum,
        'FlatNum': apartment.FlatNum,
        'Price': str(apartment.Price),
        'RoomCount': apartment.RoomCount,
        'Description': apartment.Description,
        'Comfort': apartment.Comfort,
        'Infrastructure': apartment.Infrastructure,
        'Renovation': apartment.Renovation,
        'Appliances': apartment.Appliances,
        'MaxResidents': apartment.MaxResidents,
        'CurrentResidents': apartment.CurrentResidents,
        'IsRented': apartment.IsRented,
        'CreationDate': apartment.CreationDate,
        'LastUpdated': apartment.LastUpdated,
        'FavoriteCount': apartment.FavoriteCount
    }


@apartments_api_bp.route('/apartments', methods=['GET'])
def get_apartments():
    apartments = Apartment.query.all()
    return jsonify([serialize_apartment(apartment) for apartment in apartments]), 200


@apartments_api_bp.route('/apartments/<int:apartment_id>', methods=['GET'])
def get_apartment(apartment_id):
    apartment = Apartment.query.get_or_404(apartment_id)
    return jsonify(serialize_apartment(apartment)), 200


@apartments_api_bp.route('/apartments', methods=['POST'])
def create_apartment():
    data = request.get_json()
    new_apartment = Apartment(
        OwnerId=data['OwnerId'],
        Type=data['Type'],
        City=data['City'],
        Street=data['Street'],
        HouseNum=data['HouseNum'],
        FlatNum=data.get('FlatNum', None),
        Price=data['Price'],
        RoomCount=data['RoomCount'],
        Description=data.get('Description', None),
        Comfort=data.get('Comfort', None),
        Infrastructure=data.get('Infrastructure', None),
        Renovation=data.get('Renovation', None),
        Appliances=data.get('Appliances', None),
        MaxResidents=data['MaxResidents'],
        CurrentResidents=data['CurrentResidents'],
        IsRented=data['IsRented'],
        FavoriteCount=data.get('FavoriteCount', 0)
    )
    db.session.add(new_apartment)
    db.session.commit()
    return jsonify({'message': 'Apartment created', 'ApartmentId': new_apartment.ApartmentId}), 201


@apartments_api_bp.route('/apartments/<int:apartment_id>', methods=['PUT'])
def update_apartment(apartment_id):
    data = request.get_json()
    apartment = Apartment.query.get_or_404(apartment_id)
    apartment.OwnerId = data.get('OwnerId', apartment.OwnerId)
    apartment.Type = data.get('Type', apartment.Type)
    apartment.City = data.get('City', apartment.City)
    apartment.Street = data.get('Street', apartment.Street)
    apartment.HouseNum = data.get('HouseNum', apartment.HouseNum)
    apartment.FlatNum = data.get('FlatNum', apartment.FlatNum)
    apartment.Price = data.get('Price', apartment.Price)
    apartment.RoomCount = data.get('RoomCount', apartment.RoomCount)
    apartment.Description = data.get('Description', apartment.Description)
    apartment.Comfort = data.get('Comfort', apartment.Comfort)
    apartment.Infrastructure = data.get('Infrastructure', apartment.Infrastructure)
    apartment.Renovation = data.get('Renovation', apartment.Renovation)
    apartment.Appliances = data.get('Appliances', apartment.Appliances)
    apartment.MaxResidents = data.get('MaxResidents', apartment.MaxResidents)
    apartment.CurrentResidents = data.get('CurrentResidents', apartment.CurrentResidents)
    apartment.IsRented = data.get('IsRented', apartment.IsRented)
    apartment.FavoriteCount = data.get('FavoriteCount', apartment.FavoriteCount)
    db.session.commit()
    return jsonify({'message': 'Apartment updated'}), 200


@apartments_api_bp.route('/apartments/<int:apartment_id>', methods=['DELETE'])
def delete_apartment(apartment_id):
    apartment = Apartment.query.get_or_404(apartment_id)
    db.session.delete(apartment)
    db.session.commit()
    return jsonify({'message': 'Apartment deleted'}), 200
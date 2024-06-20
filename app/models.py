# app/models.py

from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_student = db.Column(db.Boolean, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20))
    user_type = db.Column(db.Enum('орендар', 'власник'), nullable=False)
    registration_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)


class Apartment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    street = db.Column(db.String(255), nullable=False)
    house_num = db.Column(db.String(20), nullable=False)
    flat_num = db.Column(db.String(20))
    price = db.Column(db.Numeric(10, 2), nullable=False)
    room_count = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    comfort = db.Column(db.Text)
    infrastructure = db.Column(db.Text)
    renovation = db.Column(db.Text)
    appliances = db.Column(db.Text)
    max_residents = db.Column(db.Integer, nullable=False)
    current_residents = db.Column(db.Integer, nullable=False)
    is_rented = db.Column(db.Enum('вільна', 'зайнята', 'відкрита для співмешканців'), nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    last_updated = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(),
                             onupdate=db.func.current_timestamp(), nullable=False)
    favorite_count = db.Column(db.Integer, default=0)

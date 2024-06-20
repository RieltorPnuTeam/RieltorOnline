# app/models.py

from app import db


class User(db.Model):
    __tablename__ = 'users'

    UserID = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(255), unique=True, nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    IsStudent = db.Column(db.Boolean, nullable=False)
    Name = db.Column(db.String(255), nullable=False)
    PhoneNumber = db.Column(db.String(20))
    UserType = db.Column(db.Enum('орендар', 'власник'), nullable=False)
    RegistrationDate = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)


class Apartment(db.Model):
    __tablename__ = 'apartments'

    ApartmentId = db.Column(db.Integer, primary_key=True)
    OwnerId = db.Column(db.Integer, db.ForeignKey('users.UserID'), nullable=False)
    Type = db.Column(db.String(50), nullable=False)
    City = db.Column(db.String(255), nullable=False)
    Street = db.Column(db.String(255), nullable=False)
    HouseNum = db.Column(db.String(20), nullable=False)
    FlatNum = db.Column(db.String(20))
    Price = db.Column(db.Numeric(10, 2), nullable=False)
    RoomCount = db.Column(db.Integer, nullable=False)
    Description = db.Column(db.Text)
    Comfort = db.Column(db.Text)
    Infrastructure = db.Column(db.Text)
    Renovation = db.Column(db.Text)
    Appliances = db.Column(db.Text)
    MaxResidents = db.Column(db.Integer, nullable=False)
    CurrentResidents = db.Column(db.Integer, nullable=False)
    IsRented = db.Column(db.Enum('вільна', 'зайнята', 'відкрита для співмешканців'), nullable=False)
    CreationDate = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    LastUpdated = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(),
                             onupdate=db.func.current_timestamp(), nullable=False)
    FavoriteCount = db.Column(db.Integer, default=0)

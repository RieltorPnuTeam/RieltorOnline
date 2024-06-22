# app/models.py
import os

from PIL import Image
from flask import current_app

from app import db, bcrypt, login_manager, app
from flask_login import UserMixin

base_path = os.path.join(current_app.root_path, '..', '..', 'static', 'profile_pic')


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    UserID = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(255), unique=True, nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    IsStudent = db.Column(db.Boolean, nullable=False)
    Name = db.Column(db.String(255), nullable=False)
    PhoneNumber = db.Column(db.String(20))
    UserType = db.Column(db.Enum('орендар', 'власник', 'admin'), nullable=False)
    RegistrationDate = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    UserImage = db.Column(db.String(255))

    comments_written = db.relationship('UserComment', foreign_keys='UserComment.AuthorID', backref='author', lazy=True)
    comments_received = db.relationship('UserComment', foreign_keys='UserComment.TargetUserID', backref='target_user',
                                        lazy=True)
    liked_apartments = db.relationship('Apartment', secondary='favorites',
                                       backref=db.backref('liked_by_users', lazy='dynamic'))

    def __init__(self, Email, Password, IsStudent, Name, UserType, PhoneNumber=None, UserImage=None):
        self.Email = Email
        self.Password = bcrypt.generate_password_hash(Password).decode('utf-8')
        self.IsStudent = IsStudent
        self.Name = Name
        self.PhoneNumber = PhoneNumber
        self.UserType = UserType
        self.UserImage = UserImage

    def __repr__(self):
        return f"<User {self.Email}>"

    def check_password(self, password):
        return bcrypt.check_password_hash(self.Password, password)

    def get_id(self):
        return str(self.UserID)

    def save_profile_pic(self, profile_image):
        picture_fn = f'{self.UserID}.png'
        picture_path = os.path.join(current_app.root_path, 'static/profile_pic', picture_fn)

        output_size = (250, 250)
        img = Image.open(profile_image)
        img.thumbnail(output_size)
        img.save(picture_path)

        self.UserImage = picture_fn

    def set_password(self, password):
        self.Password = bcrypt.generate_password_hash(password).decode('utf-8')

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


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

    images = db.relationship('ApartmentImage', back_populates='apartment',
                             overlaps="images,images_apartment")


class ApartmentImage(db.Model):
    __tablename__ = 'apartment_images'

    ImageID = db.Column(db.Integer, primary_key=True)
    ApartmentID = db.Column(db.Integer, db.ForeignKey('apartments.ApartmentId'), nullable=False)
    ImageURL = db.Column(db.String(255), nullable=False)

    apartment = db.relationship('Apartment', backref='apartment_images')

    def __repr__(self):
        return f"<ApartmentImage(apartment_id={self.ApartmentID}, image_url='{self.ImageURL}')>"


class UserComment(db.Model):
    __tablename__ = 'usercomments'

    CommentID = db.Column(db.Integer, primary_key=True)
    AuthorID = db.Column(db.Integer, db.ForeignKey('users.UserID'), nullable=False)
    TargetUserID = db.Column(db.Integer, db.ForeignKey('users.UserID'), nullable=False)
    Content = db.Column(db.Text, nullable=False)
    Rating = db.Column(db.Integer, nullable=False)
    DateAdded = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)


class ApartmentComment(db.Model):
    __tablename__ = 'apartmentcomments'

    CommentID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('users.UserID'), nullable=False)
    ApartmentID = db.Column(db.Integer, db.ForeignKey('apartments.ApartmentId'), nullable=False)
    Content = db.Column(db.Text, nullable=False)
    Rating = db.Column(db.Integer, nullable=False)
    DateAdded = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    user = db.relationship('User', backref='apartment_comments')
    apartment = db.relationship('Apartment', backref='apartment_comments')


class Favorite(db.Model):
    __tablename__ = 'favorites'

    FavoriteID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('users.UserID'), nullable=False)
    ApartmentID = db.Column(db.Integer, db.ForeignKey('apartments.ApartmentId'), nullable=False)

    user = db.relationship('User', backref=db.backref('favorites', lazy='dynamic'))
    apartment = db.relationship('Apartment', backref=db.backref('favorites', lazy='dynamic'))


class Roommate(db.Model):
    __tablename__ = 'roommates'

    RoommateID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('users.UserID'), nullable=False)
    ApartmentID = db.Column(db.Integer, db.ForeignKey('apartments.ApartmentId'), nullable=False)

    User = db.relationship('User', backref=db.backref('roommates', cascade='all, delete-orphan'))
    Apartment = db.relationship('Apartment', backref=db.backref('roommates', cascade='all, delete-orphan'))

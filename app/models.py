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
    UserImage = db.Column(db.String(255))

    comments_written = db.relationship('UserComment', foreign_keys='UserComment.AuthorID', backref='author', lazy=True)
    comments_received = db.relationship('UserComment', foreign_keys='UserComment.TargetUserID', backref='target_user',
                                        lazy=True)


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

    Images = db.relationship('ApartmentImage', backref='apartment', lazy=True)


class ApartmentImage(db.Model):
    __tablename__ = 'apartment_images'

    ImageID = db.Column(db.Integer, primary_key=True)
    ApartmentID = db.Column(db.Integer, db.ForeignKey('apartments.ApartmentId'), nullable=False)
    ImageURL = db.Column(db.String(255), nullable=False)


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


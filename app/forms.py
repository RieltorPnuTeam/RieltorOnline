# app/forms.py

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, MultipleFileField
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.fields.numeric import DecimalField, IntegerField, FloatField
from wtforms.fields.simple import TextAreaField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, NumberRange, Regexp


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6),
        Regexp('^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$',
               message='Password must contain at least one letter and one number')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    name = StringField('Name', validators=[
        DataRequired(),
        Regexp('^[A-Z][a-z]*\s[A-Z][a-z]*$',
               message='Name must contain at least two words, each starting with a capital letter')
    ])
    phone_number = StringField('Phone Number', validators=[
        DataRequired(),
        Regexp(r'^\+\d{12}$',
               message='Invalid phone number format. Use digits only, optionally starting with + and followed by at least 10 digits')
    ])
    user_type = SelectField('User Type', choices=[('орендар', 'Орендар'), ('власник', 'Власник')],
                            validators=[DataRequired()])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class EditProfileForm(FlaskForm):
    name = StringField('Name', validators=[
        Optional(),
        Regexp('^[A-Z][a-z]*\s[A-Z][a-z]*$',
               message='Name must contain at least two words, each starting with a capital letter')
    ])
    phone_number = StringField('Phone Number', validators=[
        Optional(),
        Regexp(r'^\+\d{12}$',
               message='Invalid phone number format. Use digits only, optionally starting with + and followed by at least 10 digits')
    ])
    user_type = SelectField('User Type', choices=[('орендар', 'Орендар'), ('власник', 'Власник')],
                            validators=[DataRequired()])
    password = PasswordField('Password', validators=[
        Optional(),
        Length(min=6),
        Regexp('^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$',
               message='Password must contain at least one letter and one number')
    ])
    profile_image = FileField('Profile Image', validators=[FileAllowed(['jpg', 'png'])])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Update Profile')


class ApartmentForm(FlaskForm):
    type = SelectField('Type', choices=[('квартира', 'Квартира'), ('приватний будинок', 'Приватний будинок')],
                       validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    house_num = IntegerField('House Number', validators=[DataRequired()])
    flat_num = IntegerField('Flat Number')
    price = FloatField('Price', validators=[DataRequired()])
    room_count = IntegerField('Room Count', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    comfort = TextAreaField('Comfort', validators=[DataRequired()])
    infrastructure = TextAreaField('Infrastructure', validators=[DataRequired()])
    renovation = TextAreaField('Renovation', validators=[DataRequired()])
    appliances = TextAreaField('Appliances', validators=[DataRequired()])
    max_residents = IntegerField('Max Residents', validators=[DataRequired()])
    current_residents = IntegerField('Current Residents')
    is_rented = SelectField('Type', choices=[('вільна', 'Вільна'), ('зайнята', 'Зайнята'),
                                             ('відкрита для співмешканців', 'Відкрита для співмешканців')],
                            validators=[DataRequired()])
    images = MultipleFileField('Images')
    submit = SubmitField('Submit')


class EditApartmentForm(FlaskForm):
    type = SelectField('Type', choices=[('квартира', 'Квартира'), ('приватний будинок', 'Приватний будинок')],
                       validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    house_num = IntegerField('House Number', validators=[DataRequired()])
    flat_num = IntegerField('Flat Number')
    price = FloatField('Price', validators=[DataRequired()])
    room_count = IntegerField('Room Count', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    comfort = TextAreaField('Comfort', validators=[DataRequired()])
    infrastructure = TextAreaField('Infrastructure', validators=[DataRequired()])
    renovation = TextAreaField('Renovation', validators=[DataRequired()])
    appliances = TextAreaField('Appliances', validators=[DataRequired()])
    max_residents = IntegerField('Max Residents', validators=[DataRequired()])
    current_residents = IntegerField('Current Residents')
    is_rented = SelectField('Status', choices=[('вільна', 'Вільна'), ('зайнята', 'Зайнята'),
                                               ('відкрита для співмешканців', 'Відкрита для співмешканців')],
                            validators=[DataRequired()])
    images = MultipleFileField('Images')
    submit = SubmitField('Submit')

    '''def populate_obj(self, apartment):
        apartment.type = self.type.data
        apartment.city = self.city.data
        apartment.street = self.street.data
        apartment.house_num = self.house_num.data
        apartment.flat_num = self.flat_num.data
        apartment.price = self.price.data
        apartment.room_count = self.room_count.data
        apartment.description = self.description.data
        apartment.comfort = self.comfort.data
        apartment.infrastructure = self.infrastructure.data
        apartment.renovation = self.renovation.data
        apartment.appliances = self.appliances.data
        apartment.max_residents = self.max_residents.data
        apartment.current_residents = self.current_residents.data
        apartment.is_rented = self.is_rented.data'''


class CommentForm(FlaskForm):
    Content = TextAreaField('Comment', validators=[DataRequired()])
    Rating = IntegerField('Rating', validators=[DataRequired(), NumberRange(min=1, max=5)])
    submit = SubmitField('Submit')


class ApartmentCommentForm(FlaskForm):
    Content = TextAreaField('Comment', validators=[DataRequired()])
    Rating = IntegerField('Rating', validators=[DataRequired(), NumberRange(min=1, max=5)])
    Submit = SubmitField('Submit')


class AddRoommateForm(FlaskForm):
    email = StringField('User Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Add Roommate')

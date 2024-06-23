# app/routes/main

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt, app
from app.forms import RegistrationForm, LoginForm, EditProfileForm, CommentForm
from app.models import User, UserComment, Apartment

main_bp = Blueprint('main', __name__)


@main_bp.route('/search', methods=['GET'])
def search():
    return render_template('search.html')


@app.route('/search_results', methods=['GET'])
def search_results():
    city = request.args.get('city')
    type = request.args.get('type')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    min_rooms = request.args.get('min_rooms')
    max_rooms = request.args.get('max_rooms')
    is_rented = request.args.get('is_rented')

    query = Apartment.query

    if city:
        query = query.filter(Apartment.City.ilike(f"%{city}%"))
    if type:
        query = query.filter(Apartment.Type == type)
    if min_price:
        query = query.filter(Apartment.Price >= min_price)
    if max_price:
        query = query.filter(Apartment.Price <= max_price)
    if min_rooms:
        query = query.filter(Apartment.RoomCount >= min_rooms)
    if max_rooms:
        query = query.filter(Apartment.RoomCount <= max_rooms)
    if is_rented:
        query = query.filter(Apartment.IsRented == is_rented)

    apartments = query.all()

    return render_template('search_results.html', apartments=apartments)


@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        liked_apartments = Apartment.query.order_by(Apartment.FavoriteCount.desc()).all()
        return render_template('index.html', liked_apartments=liked_apartments)
    else:
        return redirect(url_for('main.login'))


@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(Email=form.email.data).first()
        if existing_user:
            flash('Email address already exists. Please use a different email.', 'danger')
            return redirect(url_for('main.register'))

        student_domains = ['knu.ua', 'nung.edu.ua', 'ukd.edu.ua', 'nure.ua', 'chnu.edu.ua', 'lpnu.ua', 'ucu.edu.ua',
                           'ifnmu.edu.ua', 'pnu.edu.ua']
        is_student = any(form.email.data.endswith(domain) for domain in student_domains)

        user = User(Email=form.email.data, Password=form.password.data, Name=form.name.data, IsStudent=is_student,
                    UserType=form.user_type.data, PhoneNumber=form.phone_number.data)

        db.session.add(user)
        db.session.commit()

        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('main.login'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error in {getattr(form, field).label.text}: {error}', 'danger')

    return render_template('register.html', title='Register', form=form)


@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(Email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.Name = form.name.data
        current_user.PhoneNumber = form.phone_number.data
        current_user.UserType = form.user_type.data
        if form.password.data:
            current_user.set_password(form.password.data)
        if form.profile_image.data:
            current_user.save_profile_pic(form.profile_image.data)
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('main.profile'))
    elif request.method == 'GET':
        form.name.data = current_user.Name
        form.phone_number.data = current_user.PhoneNumber
        form.user_type.data = current_user.UserType

    liked_apartments = current_user.liked_apartments
    profile_image = url_for('static', filename=f'profile_pic/{current_user.UserImage}')
    comments_received = current_user.comments_received

    return render_template('profile.html', title='Edit Profile', form=form, profile_image=profile_image,
                           comments_received=comments_received, liked_apartments=liked_apartments)


@main_bp.route('/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def user_comments(user_id):
    user = User.query.get_or_404(user_id)
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        comment = UserComment(
            AuthorID=current_user.UserID,
            TargetUserID=user.UserID,
            Content=comment_form.Content.data,
            Rating=comment_form.Rating.data
        )
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added.', 'success')
        return redirect(url_for('main.user_comments', user_id=user.UserID))
    return render_template('user.html', user=user, comment_form=comment_form)

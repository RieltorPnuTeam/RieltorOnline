from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt, app
from app.forms import RegistrationForm, LoginForm, EditProfileForm
from app.models import User

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('index.html')


@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        student_domains = ['knu.ua', 'nung.edu.ua', 'ukd.edu.ua', 'nure.ua', 'chnu.edu.ua', 'lpnu.ua', 'ucu.edu.ua',
                           'ifnmu.edu.ua', 'pnu.edu.ua']
        is_student = any(form.email.data.endswith(domain) for domain in student_domains)

        user = User(Email=form.email.data, Password=form.password.data, Name=form.name.data, IsStudent=is_student,
                    UserType=form.user_type.data, PhoneNumber=form.phone_number.data)

        db.session.add(user)
        db.session.commit()

        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('main.login'))

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

    return render_template('profile.html', title='Edit Profile', form=form, profile_image=profile_image, comments_received=comments_received, liked_apartments=liked_apartments)

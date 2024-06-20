# app/routes.py

from flask import Blueprint, render_template

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/search')
def search():
    return render_template('search.html')


@bp.route('/apartment/<int:apartment_id>')
def apartment(apartment_id):
    return render_template('apartment.html', apartment_id=apartment_id)


@bp.route('/add_apartment')
def add_apartment():
    return render_template('add_apartment.html')


@bp.route('/user/<int:user_id>')
def user_profile(user_id):
    return render_template('user.html', user_id=user_id)


@bp.route('/profile')
def profile():
    return render_template('profile.html')


@bp.route('/update_profile')
def update_profile():
    return render_template('update_profile.html')


@bp.route('/update_apartment/<int:apartment_id>')
def update_apartment(apartment_id):
    return render_template('update_apartment.html', apartment_id=apartment_id)


@bp.route('/register')
def register():
    return render_template('register.html')


@bp.route('/login')
def login():
    return render_template('login.html')

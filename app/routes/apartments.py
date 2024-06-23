# app/routes/apartments

import uuid

from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, current_app
from flask_login import login_required, current_user
from app import db, app
from app.forms import ApartmentForm, EditApartmentForm, ApartmentCommentForm, AddRoommateForm
from app.models import Apartment, ApartmentImage, User, ApartmentComment, Roommate
import os
from werkzeug.utils import secure_filename

apartment_bp = Blueprint('apartment', __name__)


@apartment_bp.route('/apartment/<int:apartment_id>', methods=['GET', 'POST'])
def view_apartment(apartment_id):
    apartment = Apartment.query.get_or_404(apartment_id)
    owner = User.query.get(apartment.OwnerId)
    comment_form = ApartmentCommentForm()

    if request.method == 'POST' and comment_form.validate_on_submit():
        if current_user.is_authenticated:
            comment = ApartmentComment(
                Content=comment_form.Content.data,
                Rating=comment_form.Rating.data,
                UserID=current_user.UserID,
                ApartmentID=apartment.ApartmentId
            )
            db.session.add(comment)
            db.session.commit()
            flash('Your comment has been added.', 'success')
            return redirect(url_for('apartment.view_apartment', apartment_id=apartment.ApartmentId))
        else:
            flash('You need to log in to comment.', 'danger')
            return redirect(url_for('users.login'))

    comments = ApartmentComment.query.filter_by(ApartmentID=apartment_id).all()
    roommates = Roommate.query.filter_by(ApartmentID=apartment_id).all()
    return render_template('apartment.html', apartment=apartment, owner=owner, comment_form=comment_form,
                           comments=comments, roommates=roommates)


@apartment_bp.route('/apartment/<int:apartment_id>/like', methods=['POST'])
@login_required
def like_apartment(apartment_id):
    apartment = Apartment.query.get_or_404(apartment_id)
    if apartment not in current_user.liked_apartments:
        current_user.liked_apartments.append(apartment)
        apartment.FavoriteCount += 1
        db.session.commit()
        flash('Apartment added to favorites!', 'success')
    else:
        flash('Apartment already in favorites!', 'info')
    return redirect(url_for('apartment.view_apartment', apartment_id=apartment_id))


@apartment_bp.route('/apartment/<int:apartment_id>/unlike', methods=['POST'])
@login_required
def unlike_apartment(apartment_id):
    apartment = Apartment.query.get_or_404(apartment_id)
    if apartment in current_user.liked_apartments:
        current_user.liked_apartments.remove(apartment)
        apartment.FavoriteCount -= 1
        db.session.commit()
        flash('Apartment removed from favorites!', 'success')
    else:
        flash('Apartment not in favorites!', 'info')
    return redirect(url_for('apartment.view_apartment', apartment_id=apartment_id))


@apartment_bp.route('/apartment/new', methods=['GET', 'POST'])
@login_required
def new_apartment():
    form = ApartmentForm()
    if form.validate_on_submit():
        apartment = Apartment(
            OwnerId=current_user.UserID,
            Type=form.type.data,
            City=form.city.data,
            Street=form.street.data,
            HouseNum=form.house_num.data,
            FlatNum=form.flat_num.data,
            Price=form.price.data,
            RoomCount=form.room_count.data,
            Description=form.description.data,
            Comfort=form.comfort.data,
            Infrastructure=form.infrastructure.data,
            Renovation=form.renovation.data,
            Appliances=form.appliances.data,
            MaxResidents=form.max_residents.data,
            CurrentResidents=form.current_residents.data,
            IsRented=form.is_rented.data
        )

        db.session.add(apartment)
        db.session.commit()

        if form.images.data:
            images = request.files.getlist(form.images.name)
            for image in images:
                if image and allowed_file(image.filename):
                    filename = secure_filename(image.filename)
                    unique_filename = f"{uuid.uuid4().hex}_{filename}"
                    filepath = os.path.join(current_app.root_path, 'static/apartment_pic', unique_filename)
                    image.save(filepath)
                    apartment_image = ApartmentImage(ApartmentID=apartment.ApartmentId, ImageURL=unique_filename)
                    db.session.add(apartment_image)

            db.session.commit()

        flash('Apartment created successfully!', 'success')
        return redirect(url_for('main.index'))
    return render_template('add_apartment.html', title='New Apartment', form=form)


@apartment_bp.route('/apartment/<int:apartment_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_apartment(apartment_id):
    apartment = Apartment.query.get_or_404(apartment_id)
    if apartment.OwnerId != current_user.UserID:
        abort(403)

    form = EditApartmentForm()
    add_roommate_form = AddRoommateForm()

    if form.validate_on_submit() and 'submit' in request.form:
        apartment.Type = form.type.data
        apartment.City = form.city.data
        apartment.Street = form.street.data
        apartment.HouseNum = form.house_num.data
        apartment.FlatNum = form.flat_num.data
        apartment.Price = form.price.data
        apartment.RoomCount = form.room_count.data
        apartment.Description = form.description.data
        apartment.Comfort = form.comfort.data
        apartment.Infrastructure = form.infrastructure.data
        apartment.Renovation = form.renovation.data
        apartment.Appliances = form.appliances.data
        apartment.MaxResidents = form.max_residents.data
        apartment.CurrentResidents = form.current_residents.data
        apartment.IsRented = form.is_rented.data

        db.session.commit()
        deleted_images_ids = request.form.getlist('deleted_images')
        if deleted_images_ids:
            for image_id in deleted_images_ids:
                image = ApartmentImage.query.get(image_id)
                if image:
                    image_path = os.path.join(current_app.root_path, 'static/apartment_pic', image.ImageURL)
                    if os.path.exists(image_path):
                        os.remove(image_path)
                    db.session.delete(image)

        if form.images.data:
            for image in request.files.getlist(form.images.name):
                if image and allowed_file(image.filename):
                    filename = secure_filename(image.filename)
                    unique_filename = f"{uuid.uuid4().hex}_{filename}"
                    filepath = os.path.join(current_app.root_path, 'static/apartment_pic', unique_filename)
                    image.save(filepath)
                    apartment_image = ApartmentImage(ApartmentID=apartment.ApartmentId, ImageURL=unique_filename)
                    db.session.add(apartment_image)

        db.session.commit()
        flash('Apartment updated successfully!', 'success')
        return redirect(url_for('apartment.view_apartment', apartment_id=apartment_id))

    if add_roommate_form.validate_on_submit() and 'add_roommate' in request.form:
        roommate_email = add_roommate_form.email.data
        roommate_user = User.query.filter_by(Email=roommate_email).first()
        if roommate_user:
            new_roommate = Roommate(ApartmentID=apartment_id, UserID=roommate_user.UserID)
            db.session.add(new_roommate)
            db.session.commit()
            flash('Roommate added successfully!', 'success')
            return redirect(url_for('apartment.view_apartment', apartment_id=apartment_id))
        else:
            flash('User with this email does not exist.', 'danger')

    form.type.data = apartment.Type
    form.city.data = apartment.City
    form.street.data = apartment.Street
    form.house_num.data = apartment.HouseNum
    form.flat_num.data = apartment.FlatNum
    form.price.data = apartment.Price
    form.room_count.data = apartment.RoomCount
    form.description.data = apartment.Description
    form.comfort.data = apartment.Comfort
    form.infrastructure.data = apartment.Infrastructure
    form.renovation.data = apartment.Renovation
    form.appliances.data = apartment.Appliances
    form.max_residents.data = apartment.MaxResidents
    form.current_residents.data = apartment.CurrentResidents
    form.is_rented.data = apartment.IsRented

    return render_template('update_apartment.html', form=form, apartment=apartment, add_roommate_form=add_roommate_form)


@apartment_bp.route('/apartment/<int:apartment_id>/roommate/delete/<int:roommate_id>', methods=['POST'])
@login_required
def delete_roommate(apartment_id, roommate_id):
    apartment = Apartment.query.get_or_404(apartment_id)
    if apartment.OwnerId != current_user.UserID:
        abort(403)

    roommate = Roommate.query.get_or_404(roommate_id)
    if roommate.ApartmentID != apartment_id:
        flash('This roommate is not related to this apartment.', 'danger')
        return redirect(url_for('apartment.edit_apartment', apartment_id=apartment_id))

    try:
        db.session.delete(roommate)
        db.session.commit()
        flash('Roommate removed successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting a roommate: {str(e)}', 'danger')

    return redirect(url_for('apartment.edit_apartment', apartment_id=apartment_id))


@apartment_bp.route('/apartment/<int:apartment_id>/delete', methods=['POST'])
@login_required
def delete_apartment(apartment_id):
    apartment = Apartment.query.get_or_404(apartment_id)
    if apartment.OwnerId != current_user.UserID:
        abort(403)
    try:
        for image in apartment.apartment_images:
            image_path = os.path.join(current_app.root_path, 'static/apartment_pic', image.ImageURL)
            if os.path.exists(image_path):
                os.remove(image_path)
            db.session.delete(image)
        db.session.delete(apartment)
        db.session.commit()
        flash('Apartment has been deleted!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting apartment: {e}', 'danger')

    return redirect(url_for('main.index'))


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

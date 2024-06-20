# app/API/apartmentcomments_api.py

from flask import Blueprint, jsonify, request, abort
from app.models import ApartmentComment, db

apartmentcomments_api_bp = Blueprint('apartmentcomments_api', __name__, url_prefix='/api')


def serialize_apartment_comment(comment):
    return {
        'CommentID': comment.CommentID,
        'UserID': comment.UserID,
        'ApartmentID': comment.ApartmentID,
        'Content': comment.Content,
        'Rating': comment.Rating,
        'DateAdded': comment.DateAdded
    }


@apartmentcomments_api_bp.route('/apartmentcomments', methods=['GET'])
def get_apartment_comments():
    comments = ApartmentComment.query.all()
    return jsonify([serialize_apartment_comment(comment) for comment in comments]), 200


@apartmentcomments_api_bp.route('/apartmentcomments/<int:comment_id>', methods=['GET'])
def get_apartment_comment(comment_id):
    comment = ApartmentComment.query.get_or_404(comment_id)
    return jsonify(serialize_apartment_comment(comment)), 200


@apartmentcomments_api_bp.route('/apartmentcomments', methods=['POST'])
def create_apartment_comment():
    data = request.get_json()
    new_comment = ApartmentComment(
        UserID=data['UserID'],
        ApartmentID=data['ApartmentID'],
        Content=data['Content'],
        Rating=data['Rating']
    )
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({'message': 'Comment created', 'CommentID': new_comment.CommentID}), 201


@apartmentcomments_api_bp.route('/apartmentcomments/<int:comment_id>', methods=['PUT'])
def update_apartment_comment(comment_id):
    data = request.get_json()
    comment = ApartmentComment.query.get_or_404(comment_id)
    comment.Content = data.get('Content', comment.Content)
    comment.Rating = data.get('Rating', comment.Rating)
    db.session.commit()
    return jsonify({'message': 'Comment updated'}), 200


@apartmentcomments_api_bp.route('/apartmentcomments/<int:comment_id>', methods=['DELETE'])
def delete_apartment_comment(comment_id):
    comment = ApartmentComment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return jsonify({'message': 'Comment deleted'}), 200

# app/API/usercomments_api.py

from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import jwt_required
from app.models import UserComment
from app import db

usercomments_api_bp = Blueprint('usercomments_api', __name__, url_prefix='/api')


def serialize_user_comment(comment):
    return {
        'CommentID': comment.CommentID,
        'AuthorID': comment.AuthorID,
        'TargetUserID': comment.TargetUserID,
        'Content': comment.Content,
        'Rating': comment.Rating,
        'DateAdded': comment.DateAdded
    }


@usercomments_api_bp.route('/usercomments', methods=['GET'])
@jwt_required()
def get_comments():
    comments = UserComment.query.all()
    return jsonify([serialize_user_comment(comment) for comment in comments]), 200


@usercomments_api_bp.route('/usercomments/<int:comment_id>', methods=['GET'])
@jwt_required()
def get_comment(comment_id):
    comment = UserComment.query.get_or_404(comment_id)
    return jsonify(serialize_user_comment(comment)), 200


@usercomments_api_bp.route('/usercomments', methods=['POST'])
@jwt_required()
def create_comment():
    data = request.get_json()
    new_comment = UserComment(
        AuthorID=data['AuthorID'],
        TargetUserID=data['TargetUserID'],
        Content=data['Content'],
        Rating=data['Rating']
    )
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({'message': 'Comment created', 'CommentID': new_comment.CommentID}), 201


@usercomments_api_bp.route('/usercomments/<int:comment_id>', methods=['PUT'])
@jwt_required()
def update_comment(comment_id):
    data = request.get_json()
    comment = UserComment.query.get_or_404(comment_id)
    comment.Content = data.get('Content', comment.Content)
    comment.Rating = data.get('Rating', comment.Rating)
    db.session.commit()
    return jsonify({'message': 'Comment updated'}), 200


@usercomments_api_bp.route('/usercomments/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    comment = UserComment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return jsonify({'message': 'Comment deleted'}), 200

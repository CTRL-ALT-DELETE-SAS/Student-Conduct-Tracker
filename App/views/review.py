from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user
from App.controllers import Review

from App.controllers.review import (
    get_reviews_by_student,
    get_reviews_by_staff,
    edit_review,
    delete_review,
)

from App.database import db

review_views = Blueprint("review_views", __name__, template_folder='../templates')

@review_views.route("/reviews/student/<string:student_id>", methods=["GET"])
@jwt_required()
def get_reviews_for_student(student_id):
    reviews = get_reviews_by_student(student_id)
    if reviews:
        return jsonify([review.to_json() for review in reviews]), 200
    else:
        return "No reviews found for the student", 404

@review_views.route("/reviews/staff/<string:staff_id>", methods=["GET"])
@jwt_required()
def get_reviews_from_staff(staff_id):
    reviews = get_reviews_by_staff(staff_id)
    if reviews:
        return jsonify([review.to_json() for review in reviews]), 200
    else:
        return "No reviews found by the staff member", 404

@review_views.route("/reviews/edit/<int:review_id>", methods=["PUT"])
@jwt_required()
def review_edit(review_id):
    review = Review.query.get(review_id)
    if not review:
        return "Review not found", 404

    if jwt_current_user.is_authenticated and current_user == review.reviewer:
        data = request.get_json()
        is_positive = data.get("isPositive")
        comment = data.get("comment")
        if is_positive is not None and comment is not None:
            review.isPositive = is_positive
            review.comment = comment
            db.session.commit()
            return jsonify(review.to_json()), 200
        else:
            return "Invalid request data", 400
    else:
        return "Unauthorized to edit this review", 401

@review_views.route("/reviews/delete/<int:review_id>", methods=["DELETE"])
def review_delete(review_id):
    review = Review.query.get(review_id)
    if not review:
        return "Review not found", 404

    if current_user.is_authenticated and current_user == review.reviewer:
        db.session.delete(review)
        db.session.commit()
        return "Review deleted successfully", 200
    else:
        return "Unauthorized to delete this review", 401

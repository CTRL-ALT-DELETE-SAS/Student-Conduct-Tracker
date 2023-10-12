from flask import Blueprint, jsonify, redirect, render_template, request, abort, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user
from App.controllers import Review
from App.controllers.staff import get_staff_by_id
from App.controllers.student import search_student
from App.database import db

from App.controllers.review import (
    get_reviews_by_staff,
    edit_review,
    delete_review,
    upvoteReview,
    downvoteReview,
    get_reviews,
    get_reviews_for_student, 
    get_review
)

# Create a Blueprint for Review views
review_views = Blueprint("review_views", __name__, template_folder='../templates')

# Route to list all reviews (you can customize this route as needed)
@review_views.route('/reviews', methods=['GET'])
def list_reviews():
    reviews = get_reviews()
    return jsonify([review.to_json() for review in reviews]), 200

# Route to view a specific review and vote on it
@review_views.route('/review/<int:review_id>', methods=['GET',])
def view_review(review_id):
    review = get_review(review_id)
    if review:
        return jsonify(review.to_json())
    else: 
        return 'Review does not exist', 401 

#Route to upvote review 
@review_views.route('/review/<int:staff_id>/<int:review_id>/upvote', methods=['POST'])
def upvote (review_id, staff_id):
    if get_review(review_id):
        staff = get_staff_by_id(staff_id)
        if staff:
            current = get_review(review_id).upvotes
            upvoteReview(review_id, staff)
            if get_review(review_id).upvotes == current: 
               return jsonify(get_review(review_id).to_json(), 'Review Already Upvoted'), 201 
            else:
                return jsonify(get_review(review_id).to_json(), 'Review Upvoted'), 200 
        else: 
            return jsonify(get_review(review_id).to_json(), 'Staff does not exist'), 404     
    else: 
        return'Review does not exist'

#Route to downvote review 
@review_views.route('/review/<int:staff_id>/<int:review_id>/downvote', methods=['POST'])
def downvote (review_id, staff_id):
    if get_review(review_id):
        staff = get_staff_by_id(staff_id)
        if staff:
            current = get_review(review_id).downvotes
            downvoteReview(review_id, staff)
            if get_review(review_id).downvotes == current: 
               return jsonify(get_review(review_id).to_json(), 'Review Already Downvoted'), 201 
            else:
                return jsonify(get_review(review_id).to_json(), 'Review Downvoted'), 200 
        else: 
            return jsonify(get_review(review_id).to_json(), 'Staff does not exist'), 404      
    else: 
        return'Review does not exist'

# Route to get reviews by student ID
@review_views.route("/reviews/student/<string:student_id>", methods=["GET"])
def get_reviews_of_student(student_id):
    if search_student(student_id):
        reviews = get_reviews_for_student(student_id)
        if reviews:
            return jsonify([review.to_json() for review in reviews]), 200
        else:
            return "No reviews found for the student", 404
    return "Student does not exist", 404

# Route to get reviews by staff ID
@review_views.route("/reviews/staff/<string:staff_id>", methods=["GET"])
def get_reviews_from_staff(staff_id):
    if get_staff_by_id(staff_id):
        reviews = get_reviews_by_staff(staff_id)
        if reviews:
            return jsonify([review.to_json() for review in reviews]), 200
        else:
            return "No reviews found by the staff member", 404
    return "Staff does not exist", 404

# Route to edit a review
@review_views.route("/review/edit/<int:staff_id>/<int:review_id>/<int:isPositive>/<string:text>", methods=["PUT"])
def review_edit(review_id, staff_id, isPositive, text):
    review = get_review(review_id)
    staff = get_staff_by_id(staff_id)
    if not review:
        return "Review not found", 404

    if isPositive not in (0, 1):
        return "invalid positivity. Positive: True, False", 400 

    if review.reviewerID is not staff.ID:
        return "Not author of review", 401 

    is_positive = isPositive
    comment = text

    if comment is not None:
        edit_review(review, staff, is_positive, comment)
        return jsonify(review.to_json(), 'Review Editted'), 200
    else:
        return "Invalid request data", 400


# Route to delete a review
@review_views.route("/review/delete/<int:staff_id>/<int:review_id>", methods=["DELETE"])
def review_delete(review_id, staff_id):
    review = get_review(review_id)
    staff = get_staff_by_id(staff_id)

    if not review:
        return "Review not found", 404
    
    if review.reviewerID is not staff.ID:
        return "Not author of review", 401 
   
    if delete_review(review, staff):
        return "Review deleted successfully", 200
    else:
        return "Issues removing review", 404


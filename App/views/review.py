from flask import Blueprint, jsonify, redirect, render_template, request, abort, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user
from App.controllers import *


# Create a Blueprint for Review views
review_views = Blueprint("review_views", __name__, template_folder='../templates')

''' API Routes '''

# Route to list all reviews (you can customize this route as needed)
@review_views.route('/api/reviews', methods=['GET'])
def list_reviews_api():
    reviews = get_reviews()
    return jsonify([review.to_json() for review in reviews]), 200

# Route to view a specific review and vote on it
@review_views.route('/api/reviews/<int:review_id>', methods=['GET',])
def view_review_api(review_id):
    review = get_review(review_id)
    if review:
        return jsonify(review.to_json())
    else: 
        return 'Review does not exist', 404


#Route to upvote review 
@review_views.route('/api/reviews/<int:review_id>/upvotes', methods=['POST'])
@jwt_required()
def upvote_review_api(review_id):
    if not jwt_current_user or not isinstance(jwt_current_user, Staff):
      return "You are not authorized to upvote this review", 401
      
    review = get_review(review_id) 
    if review:
        staff = get_staff(jwt_current_user.id)
        if staff:
            current = review.upvotes
            new_votes= upvoteReview(review, staff)
            if new_votes == current: 
               return jsonify(review.to_json(), 'Review Already Upvoted'), 201 
            else:
                return jsonify(review.to_json(), 'Review Upvoted'), 200
        else: 
            return jsonify('Staff does not exist'), 404     
    else: 
        return'Review does not exist', 404

#Route to downvote review 
@review_views.route('/api/reviews/<int:review_id>/downvotes', methods=['POST'])
@jwt_required()
def downvote_review_api(review_id):
    if not jwt_current_user or not isinstance(jwt_current_user, Staff):
      return "You are not authorized to downvote this review", 401
  
    review= get_review(review_id) 
    if review:
        staff = get_staff(jwt_current_user.id)
        if staff:
            current = review.downvotes
            new_votes= downvoteReview(review, staff)
            if new_votes == current: 
               return jsonify(review.to_json(), 'Review Already Downvoted'), 201 
            else:
                return jsonify(review.to_json(), 'Review Downvoted Successfully'), 200 
        else: 
            return jsonify(get_review(review_id).to_json(), 'Staff does not exist'), 404
    else: 
        return'Review does not exist', 404


# Route to get reviews by student ID
@review_views.route("/api/students/<string:student_id>/reviews", methods=["GET"])
def get_reviews_of_student_api(student_id):
    if get_student(student_id):
        reviews = get_reviews_for_student(student_id)
        if reviews:
            return jsonify([review.to_json() for review in reviews]), 200
        else:
            return "No reviews found for the student", 404
    return "Student does not exist", 404


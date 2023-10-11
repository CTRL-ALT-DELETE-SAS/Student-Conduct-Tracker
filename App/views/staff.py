import random
import string
from flask import Blueprint, request, jsonify


from App.controllers.staff import (
    get_staff_by_id, 
    get_staff_reviews,
    search_students_searchTerm, 
    get_student_rankings,
    create_review
)

staff_views = Blueprint('staff_views', __name__, template_folder='../templates')

@staff_views.route('/staff/<int:staff_id>', methods=['GET'])
def get_staff(staff_id):
    staff = get_staff_by_id(staff_id)
    if staff:
        return jsonify(staff.to_json())
    return 'Staff not found', 404

@staff_views.route('/staff/<int:staff_id>/reviews', methods=['POST'])
def create_staff_review(staff_id):
    studentID = str(random.randint(1, 100))
    isPositive = random.choice([True, False])
    comment = ''.join(random.choices(string.ascii_letters, k=100))

    if not studentID or not comment:
            return "Invalid request data", 400

    review = create_review(staff_id, studentID, isPositive, comment)
    
    if review:
        return jsonify(review.to_json()), 201
    return 'Failed to create review', 400

@staff_views.route('/staff/<int:staff_id>/reviews', methods=['GET'])
def get_staff_reviews_endpoint(staff_id):
    reviews = get_staff_reviews(staff_id)
    return jsonify(reviews)

@staff_views.route('/staff/<string:search_term>', methods=['GET'])
def search_students(search_term):
    students = search_students_searchTerm(search_term)
    return jsonify(students)

@staff_views.route('/staff/rankings', methods=['GET'])
def get_student_rankings():
    rankings = get_student_rankings()
    return jsonify(rankings)
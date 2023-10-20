import random
import string
from flask import Blueprint, request, jsonify
from App.controllers import Student, Staff
from App.controllers.user import get_staff, get_student
from App.database import db

from App.controllers.staff import (
    search_students_searchTerm, 
    getStudentRankings,
    create_review
)

staff_views = Blueprint('staff_views', __name__, template_folder='../templates')

@staff_views.route('/staff/<int:staff_id>', methods=['GET'])
def get_staff_action(staff_id):
    staff = get_staff(staff_id)
    if staff:
        return jsonify(staff.to_json())
    return 'Staff not found', 404

@staff_views.route('/staff/<int:student_id>/reviews', methods=['POST'])
def create_staff_review(student_id):
    data = request.json

    if not get_student(student_id):
        return 'Student does not exist', 404

    if not data['staff_id'] or not data['comment']:
        return "Invalid request data", 400
    
    if data['isPositive'] not in (True, False):
        return jsonify({"message": f"invalid Positivity ({data['isPositive']}). Positive: true or false"}), 400

    if not get_staff(data['staff_id']):
        return 'Staff does not exist', 404 

    review = create_review(data['staff_id'], student_id, data['isPositive'], data['comment'])
    
    if review:
        return jsonify(review.to_json()), 201
    return 'Failed to create review', 400

@staff_views.route('/staff/student/<string:search_term>', methods=['GET'])
def search_students(search_term):
    students = search_students_searchTerm(search_term)
    return jsonify(students)

@staff_views.route('/rankings', methods=['GET'])
def get_student_rankings():
    rankings = getStudentRankings()
    return jsonify(rankings)
import random
import string
from flask import Blueprint, request, jsonify
from App.database import db
from flask_jwt_extended import current_user as jwt_current_user
from flask_jwt_extended import jwt_required
from App.controllers import *

staff_views = Blueprint('staff_views', __name__, template_folder='../templates')

''' API Routes '''

@staff_views.route('/api/reviews', methods=['POST'])
@jwt_required()
def create_review_api():
    if not jwt_current_user or not isinstance(jwt_current_user, Staff):
      return 'Unauthorized', 401
    data = request.json

    if not data['studentID']:
        return jsonify({"error": 'Student does not exist'}), 404
    
    if not data['comment']:
        return "Invalid request data", 400
    
    if data['isPositive'] not in (True, False):
        return jsonify({"message": f"invalid Positivity ({data['isPositive']}). Positive: true or false"}), 400

    if not get_staff(str(jwt_current_user.id)):
        return 'Staff does not exist', 404 

    review = create_review(jwt_current_user.id, data['studentID'], data['isPositive'], data['comment'])
    
    if review:
        return jsonify(review.to_json()), 201
    return 'Failed to create review', 400

@staff_views.route('/api/students/<string:search_term>', methods=['GET'])
@jwt_required()
def search_students(search_term):
  if jwt_current_user and isinstance(jwt_current_user, Staff): 
    students = search_students_searchTerm(jwt_current_user, search_term)
    if students:
      return jsonify([student for student in students]), 200
    else:
      return jsonify({"message": f"No students found with search term {search_term}"}), 204
  else:
    return jsonify({"message": "You are not authorized to perform this action"}), 401
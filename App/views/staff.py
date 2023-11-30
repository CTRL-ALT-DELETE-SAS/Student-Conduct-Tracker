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
    staff = get_staff(jwt_current_user.id)
    if staff:
        
      data = request.json

      if not data['studentID'] or not data['comment'] or data['isPositive'] not in (True, False):
        return jsonify(error="invalid request data"), 400
      
      student = get_student(data['studentID'])
      if not student:
        return jsonify({"error": f"student with ID {data['studentID']} does not exist"}), 400
      '''
      if not data['comment']:
          return "Invalid request data", 400
      if data['isPositive'] not in (True, False):
          return jsonify({"message": f"invalid Positivity ({data['isPositive']}). Positive: true or false"}), 400
      '''
      
      review = create_review(jwt_current_user.id, data['studentID'], data['isPositive'], data['comment'])
      
      if review:
          return jsonify(review.to_json()), 201
      return 'Failed to create review', 400

    else:
      return jsonify(error="cannot perform action"), 403

# in following API convention, the word 'search' in the route represents the noun version and not the verb version
@staff_views.route('/api/students/search', methods=['GET'])
@jwt_required()
def search_students_api():
  results = []
  staff = get_staff(jwt_current_user.id)
  if staff:
    search_query = request.args.get('query') # query params
    
    students = searchStudents(staff, search_query)
    if students:
      return jsonify(students), 200
      #return jsonify([student for student in students]), 200
    else:
      return jsonify({"message": f"No students found with search query {search_query}"}), 200
      
    
  else:
    return jsonify(error="cannot perform action"), 403
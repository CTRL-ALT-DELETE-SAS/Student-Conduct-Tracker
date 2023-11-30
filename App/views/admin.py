from flask import Blueprint, jsonify, render_template, request, send_from_directory
from flask_jwt_extended import current_user as jwt_current_user
from flask_jwt_extended import jwt_required
from flask_login import current_user

from App.controllers import *

# Create a Blueprint for user views
admin_views = Blueprint("admin_views", __name__, template_folder='../templates')

''' Page/Action Routes '''
'''
# Route to get page of all users 
@admin_views.route('/staff', methods=['GET'])
def get__all_staff_action():
    staff = get_all_staff()
    return render_template('users.html', users=users)

@admin_views.route('/static/users', methods=['GET'])
def static_user_page():
  return send_from_directory('static', 'static-user.html')

# Route to create a new student
@admin_views.route("/user/create_student", methods=["POST"])
@jwt_required()
def create_student_action():
    data = request.json #get data from post request

    if not data['firstname'] or not data['lastname'] or not data['password'] or not data['studentID'] or not data['contact'] or not data['studentType'] or not data['yearOfStudy']:
      return jsonify({"error": "Invalid request data"}), 400

      #check if id exists in the database
    if get_student(data['studentID']) or get_staff(data['studentID']) or get_admin(data['studentID']):
      return jsonify({"error": f"A user already uses the ID {data['studentID']}"}), 500

  #validate student type
    student_type = data['studentType'].strip().title()
    if student_type not in ('Full-Time', 'Part-Time', 'Evening'):
      return jsonify({"message": f"invalid student type ({data['studentType']}). Types: Full-Time, Part-Time and Evening"}), 400 

  #validate admin user
    if jwt_current_user and isinstance(jwt_current_user, Admin):
      student = create_student(jwt_current_user, data['studentID'],firstname=data['firstname'], lastname=data['lastname'], password=data['password'], contact=data['contact'], studentType=student_type, yearofStudy=data['yearOfStudy'])

      if student:
        return jsonify({"message": f"Student created with ID {student.ID}"}, student.to_json()), 201
      else: 
        return jsonify({"error": "Error creating student"}), 400
    else:
      return jsonify({"error" : "Unauthorized: You must be an admin to create students"}), 401
  
# Route to create a new staff member
@admin_views.route("/user/create_staff", methods=["POST"])
@jwt_required()
def create_staff_action():
  #get data from the post request body 
  data = request.json
  
  #validate data
  if not data['firstname'] or not data['lastname'] or not data['password'] or not data['staffID'] or not data['email'] or not data['teachingExperience']:
    return jsonify({"error": "Invalid request data"}), 400
  
  if get_student(data['staffID']) or get_staff(data['staffID']) or get_admin(data['staffID']):
    return jsonify({"error": f"A user already uses the ID {data['staffID']}"}), 400
  
  if jwt_current_user and isinstance(jwt_current_user, Admin):
    
    staff = create_staff(jwt_current_user, data['firstname'], data['lastname'], data['password'], data['staffID'], data['email'], data['teachingExperience'])
    if staff:
      return jsonify({"message": f"Staff created with ID {staff.ID}"}, staff.to_json()), 201
    else:
      return jsonify({"error": "Error creating staff"}), 400
  else:
    return jsonify({"error" : "Unauthorized: You must be an admin to create staff"}), 401


# Route to get a student by ID
@admin_views.route("/student/<string:id>", methods=["GET"])
def get_student_action(id):
    student = get_student(str(id))
    if student:
        return jsonify(student.to_json()), 200
    else:
        return "Student not found", 404


# Route to get all students
@admin_views.route("/students", methods=["GET"])
def get_all_students_action():
    students = get_all_students()
    if students:
       return jsonify([student.to_json() for student in students]), 200
    else:
        return "No students found", 404


# Route to update a student's information
@admin_views.route("/student/<string:id>/update", methods=["PUT"])
@jwt_required()
def update_student_action(id):
    if not jwt_current_user or not isinstance(jwt_current_user, Admin):
      return jsonify({"error" : "Unauthorized: You must be an admin to update students"}), 401

    student = get_student(str(id))
    if not student:
      return jsonify({"error": "Student not found"}), 404

    #if a field was not entered set it to the current value for student so it remains unchanged so no need to enter every field on the request body/form
    data = request.json
    firstname = data.get("firstname", student.firstname)
    lastname = data.get("lastname", student.lastname)
    password = data.get("password", None)
    contact = data.get("contact", student.contact)
    student_type = data.get("studentType", student.studentType)
    yearOfStudy = data.get("yearOfStudy", student.yearOfStudy)

    #Make student type case insensitive by converting to title format (1st letter in each word is uppercase)
    student_type = student_type.strip().title()
    if student_type not in ('Full-Time', 'Part-Time', 'Evening'):
        return jsonify({"message": f"invalid student type ({data['studentType']}). Types: Full-Time, Part-Time and Evening"}), 400 
  
    updated= update_student(student, firstname, lastname, password, contact, student_type, yearOfStudy)
    if updated:
      return jsonify(student.to_json(), "Student information updated successfully"), 200
    else:
      return jsonify({"error": "Error updating student"}), 400 


@admin_views.route('/identify', methods=['GET'])
@jwt_required()
def identify_user_action():
    return jsonify({'message': f"username: {current_user.fistname}, id : {current_user.ID}, type: {current_user.user_type}"})
'''

''' API Routes '''

# Route to get all users
@admin_views.route('/api/staff', methods=['GET'])
@jwt_required()
def get_all_staff_api():
  admin = get_admin(jwt_current_user.id)
  if admin:
    staff = get_all_staff_json()
    return jsonify(staff)
  return jsonify(error='cannot perform that action'), 403

# Route to get all students, both admin and staff can access this route
@admin_views.route("/api/students", methods=["GET"])
@jwt_required()
def get_all_students_api():
  admin = get_admin(jwt_current_user.id)
  staff = get_staff(jwt_current_user.id)
  if admin or staff:
    students = get_all_students_json()
    return jsonify(students)
  return jsonify(error='cannot perform that action'), 403


# Route to get a student by ID, both admin and staff can access this route
@admin_views.route("/api/students/<string:student_id>", methods=["GET"])
@jwt_required()
def get_student_api(student_id):
  student = get_student(str(student_id))
  if student:
    return jsonify(student.to_json()), 200
  else:
    return jsonify(error="student not found"), 404


# Route to get a staff by ID, both admin and staff can access this route
@admin_views.route("/api/staff/<string:staff_id>", methods=["GET"])
@jwt_required()
def get_staff_api(staff_id):
  admin = get_admin(jwt_current_user.id)
  if admin:
    staff = get_staff(str(staff_id))
    if staff:
        return jsonify(staff.to_json()), 200
    else:
        return jsonify(error="staff not found"), 404
  return jsonify(error='cannot perform that action'), 403


# Route to create a new staff member
@admin_views.route("/api/staff", methods=["POST"])
@jwt_required()
def create_staff_api():
  admin = get_admin(jwt_current_user.id)
  if admin:

    data = request.json

    if not data['id'] or not data['firstname'] or not data['lastname'] or not data['password'] or not data['email']:
      return jsonify(error="invalid request data"), 400

    if get_staff(data['id']):
      return jsonify({"error": f"a staff already uses the ID {data['id']}"}), 400  
  
    staff = create_staff(jwt_current_user, data['id'], data['firstname'], data['lastname'], data['password'], data['email'])
    if staff:
      return jsonify({"message": f"staff created with ID {data['id']}"}, staff.to_json()), 201
    else:
      return jsonify(error="error creating staff"), 400

  else:
    return jsonify(error="cannot perform that action"), 403
  

# Route to create a new student
@admin_views.route("/api/students", methods=["POST"])
@jwt_required()
def create_student_api():
  admin = get_admin(jwt_current_user.id)
  if admin:

    data = request.json

    if not data['id'] or not data['firstname'] or not data['lastname'] or not data['contact'] or not data['studentType'] or not data['yearOfStudy']:
      return jsonify(error="invalid request data"), 400

    if get_student(data['id']):
      return jsonify({"error": f"a student already uses the ID {data['id']}"}), 400

    student_type = data['studentType'].strip().title()
    if student_type not in ('Full-Time', 'Part-Time', 'Evening'):
      return jsonify({"message": f"invalid student type ({data['studentType']}). Types: Full-Time, Part-Time and Evening"}), 400   
    student = create_student(jwt_current_user, data['id'], data['firstname'], data['lastname'], data['contact'], data['studentType'], data['yearOfStudy'])

    if student:
      return jsonify({"message": f"student created with ID {data['id']}"}, student.to_json()), 201
    else:
      return jsonify(error="error creating student"), 400

  else:
    return jsonify(error="cannot perform that action"), 403
    


# Route to update a student's information
@admin_views.route("/api/students/<string:student_id>", methods=["PUT"])
@jwt_required()
def update_student_api(student_id):
  admin = get_admin(jwt_current_user.id)
  if admin:

    student = get_student(str(student_id))
    if not student:
      return jsonify(error="student not found"), 404

    #if a field was not entered set it to the current value for student so it remains unchanged so no need to enter every field on the request body/form
    data = request.json
    firstname = data.get("firstname", student.firstname)
    lastname = data.get("lastname", student.lastname)
    contact = data.get("contact", student.contact)
    studentType = data.get("studentType", student.studentType)
    yearOfStudy = data.get("yearOfStudy", student.yearOfStudy)

    #Make student type case insensitive by converting to title format (1st letter in each word is uppercase)
    studentType = studentType.strip().title()
    if studentType not in ('Full-Time', 'Part-Time', 'Evening'):
        return jsonify({"message": f"invalid student type ({data['studentType']}). Types: Full-Time, Part-Time and Evening"}), 400 
  
    updated = update_student(jwt_current_user, student, firstname, lastname, contact, studentType, yearOfStudy)
    if updated:
      return jsonify(student.to_json(), "Student information updated successfully"), 200
    else:
      return jsonify(error="error updating student"), 400

  else:
    return jsonify(error="cannot perform that action"), 403


@admin_views.route('/api/identify', methods=['GET'])
@jwt_required()
def identify_user_api():
    return jsonify({'message': f"username: {current_user.fistname}, id : {current_user.ID}, type: {current_user.user_type}"})
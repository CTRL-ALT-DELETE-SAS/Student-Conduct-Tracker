from flask import Blueprint, request, render_template, jsonify, send_from_directory 
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from App.controllers import Staff, Student
from App.controllers import *
from flask_login import current_user, login_required


# Create a Blueprint for user views
user_views = Blueprint("user_views", __name__, template_folder='../templates')

# Route to get page of all users 
@user_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

# Route to get all users
@user_views.route('/api/users', methods=['GET'])
def get_users_action():
    users = get_all_users_json()
    return jsonify(users)

@user_views.route('/static/users', methods=['GET'])
def static_user_page():
  return send_from_directory('static', 'static-user.html')

# Route to create a new student
@user_views.route("/user/create_student", methods=["POST"])
def create_student_action():
    data = request.json

    if not data['firstname'] or not data['lastname'] or not data['password'] or not data['studentID'] or not data['contact'] or not data['studentType'] or not data['yearOfStudy']:
        return "Invalid request data", 400

    if get_student(data['studentID']) or get_staff(data['studentID']) or get_admin(data['studentID']):
          return jsonify({"error": f"A user already uses the ID {data['studentID']}"}), 500
    
    if data['studentType'] not in ('Full-time', 'Part-time', 'Evening'):
        return jsonify({"message": f"invalid student type ({data['studentType']}). Types: Full-time, Part-time and Evening"}), 400 

    student = create_student(firstname=data['firstname'], lastname=data['lastname'], password=data['password'], 
                            studentID=data['studentID'], contact=data['contact'], studentType=data['studentType'], yearofStudy=data['yearOfStudy'])
    
    if student: return jsonify({"message": f"Student created with ID {student.ID}"}, student.to_json()), 201
    else: return "Error creating student", 400


# Route to create a new staff member
@user_views.route("/user/create_staff", methods=["POST"])
def create_staff_action():
	#get data from the post request body
    data = request.json

	#validate data
    if not data['firstname'] or not data['lastname'] or not data['password'] or not data['staffID'] or not data['email'] or not data['teachingExperience']:
        return "Invalid request data", 400
    
    if get_student(data['staffID']) or get_staff(data['staffID']) or get_admin(data['staffID']):
          return jsonify({"error": f"A user already uses the ID {data['staffID']}"}), 500

    staff = create_staff(data['firstname'], data['lastname'], data['password'], data['staffID'], data['email'], data['teachingExperience'])
		
    if staff: return jsonify({"message": f"Staff created with ID {staff.ID}"}, staff.to_json()), 201
    else: return "Error creating staff", 400


# Route to get a student by ID
@user_views.route("/student/<string:id>", methods=["GET"])
def get_student_action(id):
    student = get_student(id)
    if student:
        return jsonify(student.to_json()), 200
    else:
        return "Student not found", 404


# Route to get all students
@user_views.route("/students", methods=["GET"])
def get_all_students_action():
    students = get_all_students()
    if students:
       return jsonify([student.to_json() for student in students]), 200
    else:
        return "No students found", 404


# Route to get all staff members
@user_views.route("/staff", methods=["GET"])
def get_all_staff_action():
    staff = get_all_staff()
    if staff:
        return jsonify([s.to_json() for s in staff]), 200
    else:
        return "No staff members found", 404


# Route to update a student's information
@user_views.route("/update_student", methods=["PUT"])
def update_student_action():
    data = request.json

    if not data['firstname'] or not data['lastname'] or not data['password'] or not data['studentID'] or not data['contact'] or not data['studentType'] or not data['yearOfStudy']:
        return "Invalid request data", 400

    student = get_student(data['studentID'] )
    
    if student:
        if data['studentType'] not in ('Full-time', 'Part-time', 'Evening'):
            return jsonify({"message": f"invalid student type ({data['studentType']}). Types: Full-time, Part-time and Evening"}), 400 
        
        update_student(student, data['firstname'], data['lastname'], data['password'], data['contact'], data['studentType'], data['yearOfStudy'])
        return jsonify(student.to_json(), "Student information updated successfully"), 200
    else:
        return "Student not found", 404


@user_views.route('/identify', methods=['GET'])
@jwt_required()
def identify_user_action():
    return jsonify({'message': f"username: {current_user.fistname}, id : {current_user.ID}, type: {current_user.user_type}"})
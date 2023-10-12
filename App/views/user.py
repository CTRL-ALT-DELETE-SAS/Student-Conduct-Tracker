import random
from flask import Blueprint, render_template, jsonify, send_from_directory 
import randomname
from App.controllers import Staff, Student
from App.controllers.user import (
    create_student,
    create_staff,
    get_all_users,
    get_student,
    get_all_users_json,
    get_all_students,
    get_all_staff,
    update_student,
)
from App.database import db

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
@user_views.route("/create_student/<string:first_name>/<string:pass_word>", methods=["POST"])
def create_student_action(first_name, pass_word):
    firstname = first_name
    lastname = randomname.get_name()
    password = pass_word
    studentID = db.session.query(Staff).count() + db.session.query(Student).count() + 2
    contact = randomname.get_name() + '@schooling.com'
    studentType = random.choice(['Full-time','Part-time', 'evening'])
    yearOfStudy = str(random.randint(1, 8))

    if not firstname or not lastname or not password or not studentID or studentID < studentID:
        return "Invalid request data", 400

    student = create_student(
        firstname, lastname, password, studentID, contact, studentType, yearOfStudy
    )
    return jsonify(student.to_json()), 201


# Route to create a new staff member
@user_views.route("/create_staff/<string:first_name>/<string:pass_word>", methods=["POST"])
def create_staff_action(first_name, pass_word):
    firstname = first_name
    lastname = randomname.get_name()
    password = pass_word
    staffID = db.session.query(Staff).count() + db.session.query(Student).count() + 2
    email = randomname.get_name() + '@schooling.com'
    teachingExperience = str(random.randint(1, 15))

    if not firstname or not lastname or not password or not staffID or not email or staffID < staffID:
        return "Invalid request data", 400

    staff = create_staff(
            firstname, lastname, password, staffID, email, teachingExperience
        )
    return jsonify(staff.to_json()), 201

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
@user_views.route("/update_student/<int:studentID>/<string:contacts>/<string:student_type>/<int:year_of_study>", methods=["PUT"])
def update_student_action(studentID, contacts, student_type, year_of_study):
    student = get_student(studentID)
    
    if student:
        contact = contacts
        studentType = student_type
        yearofStudy = year_of_study
        
        if studentType not in ('Full-time', 'Part-time', 'Evening'):
            return "invalid student type. Types: Full-time, Part-time and Evening", 400 

        if not contact or not studentType or not yearofStudy:
            return "Invalid request data", 400
        
        update_student(student, contact, studentType, yearofStudy)
        return jsonify(student.to_json(), "Student information updated successfully"), 200
    else:
        return "Student not found", 404


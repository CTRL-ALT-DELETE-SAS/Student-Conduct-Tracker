from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_login import current_user, login_required
from App.controllers.user import (
    create_student,
    create_staff,
    create_user,
    get_staff,
    get_all_users,
    get_student,
    is_staff,
    is_student,
    is_admin,
    get_all_users_json,
    get_all_students,
    get_all_staff,
    update_student,
)
from App.database import db

# Create a Blueprint for user views
user_views = Blueprint("user_views", __name__, template_folder='../templates')

@user_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@user_views.route('/api/users', methods=['GET'])
def get_users_action():
    users = get_all_users_json()
    return jsonify(users)

@user_views.route('/api/users', methods=['POST'])
def create_user_endpoint():
    data = request.json
    create_user(data['firstname'], data['lastname'], data['password'])
    return jsonify({'message': f"user {data['firstname']} created"})

@user_views.route('/users', methods=['POST'])
def create_user_action():
    data = request.form
    flash(f"User {data['firstname']} created!")
    create_user(data['firstname'], data['lastname'], data['password'])
    return redirect(url_for('user_views.get_user_page'))

@user_views.route('/static/users', methods=['GET'])
def static_user_page():
  return send_from_directory('static', 'static-user.html')

# Route to create a new student
@user_views.route("/user/create_student", methods=["POST"])
@login_required
def create_student_action():
    if current_user.is_admin:
        data = request.get_json()
        firstname = data.get("firstname")
        lastname = data.get("lastname")
        password = data.get("password")
        id = data.get("id")
        contact = data.get("contact")
        studentType = data.get("studentType")
        yearOfStudy = data.get("yearOfStudy")

        if not firstname or not lastname or not password or not id:
            return "Invalid request data", 400

        student = create_student(
            firstname, lastname, password, id, contact, studentType, yearOfStudy
        )
        return jsonify(student.to_json()), 201
    else:
        return "Unauthorized to create a student", 401

# Route to create a new staff member
@user_views.route("/user/create_staff", methods=["POST"])
@login_required
def create_staff_action():
    if current_user.is_admin:
        data = request.get_json()
        firstname = data.get("firstname")
        lastname = data.get("lastname")
        password = data.get("password")
        id = data.get("id")
        email = data.get("email")
        teachingExperience = data.get("teachingExperience")

        if not firstname or not lastname or not password or not id or not email:
            return "Invalid request data", 400

        staff = create_staff(
            firstname, lastname, password, id, email, teachingExperience
        )
        return jsonify(staff.to_json()), 201
    else:
        return "Unauthorized to create a staff member", 401

# Route to create a new admin
@user_views.route("/user/create_admin", methods=["POST"])
@login_required
def create_admin_action():
    if current_user.is_admin:
        data = request.get_json()
        firstname = data.get("firstname")
        lastname = data.get("lastname")
        password = data.get("password")

        if not firstname or not lastname or not password:
            return "Invalid request data", 400

        admin = create_user(firstname, lastname, password)
        return jsonify(admin.to_json()), 201
    else:
        return "Unauthorized to create an admin", 401

# Route to get a staff member by ID
@user_views.route("/user/staff/<string:id>", methods=["GET"])
@login_required
def get_staff_route(id):
    staff = get_staff(id)
    if staff:
        return jsonify(staff.to_json()), 200
    else:
        return "Staff member not found", 404

# Route to get a student by ID
@user_views.route("/user/student/<string:id>", methods=["GET"])
@login_required
def get_student_action(id):
    student = get_student(id)
    if student:
        return jsonify(student.to_json()), 200
    else:
        return "Student not found", 404

# Route to check if a user is a staff member
@user_views.route("/user/is_staff/<string:id>", methods=["GET"])
@login_required
def is_staff_action(id):
    return jsonify({"is_staff": is_staff(id)}), 200

# Route to check if a user is a student
@user_views.route("/user/is_student/<string:id>", methods=["GET"])
@login_required
def is_student_action(id):
    return jsonify({"is_student": is_student(id)}), 200

# Route to check if a user is an admin
@user_views.route("/user/is_admin/<string:id>", methods=["GET"])
@login_required
def is_admin_action(id):
    return jsonify({"is_admin": is_admin(id)}), 200

# Route to get all students
@user_views.route("/user/students", methods=["GET"])
@login_required
def get_all_students_action():
    students = get_all_students()
    if students:
        return jsonify([student.to_json() for student in students]), 200
    else:
        return "No students found", 404

# Route to get all staff members
@user_views.route("/user/staff", methods=["GET"])
@login_required
def get_all_staff_action():
    staff = get_all_staff()
    if staff:
        return jsonify([s.to_json() for s in staff]), 200
    else:
        return "No staff members found", 404

# Route to update a student's information
@user_views.route("/user/update_student/<string:student_id>", methods=["PUT"])
@login_required
def update_student_action(student_id):
    if current_user.is_admin or (
        current_user.is_staff and current_user.staffID == student_id
    ):
        data = request.get_json()
        contact = data.get("contact")
        studentType = data.get("studentType")
        yearofStudy = data.get("yearofStudy")

        if not contact or not studentType or not yearofStudy:
            return "Invalid request data", 400

        result = update_student(student_id, contact, studentType, yearofStudy)
        if result:
            return "Student information updated successfully", 200
        else:
            return "Student not found", 404
    else:
        return "Unauthorized to update student information", 401
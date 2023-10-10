from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from App.database import db
from App.controllers import Student

from App.controllers.karma import (
    get_karma_by_id,
    calculate_student_karma,
    update_student_karma_rankings,
)

karma_views = Blueprint("karma_views", __name__, template_folder='../templates')

@karma_views.route("/karma/<int:karma_id>", methods=["GET"])
@jwt_required()
def get_karma(karma_id):
    karma = get_karma_by_id(karma_id)
    if karma:
        return jsonify(karma.to_json()), 200
    else:
        return "Karma not found", 404


@karma_views.route("/karma/calculate/<int:student_id>", methods=["POST"])
@jwt_required()
def calculate_student_karma_route(student_id):
    student = Student.query.get(student_id)
    if student:
        karma = calculate_student_karma(student)
        return jsonify(karma.to_json()), 200
    else:
        return "Student not found", 404


@karma_views.route("/karma/update_rankings", methods=["POST"])
def update_karma_rankings_route():
    update_student_karma_rankings()
    return "Karma rankings updated", 200

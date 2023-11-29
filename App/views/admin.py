from flask import Blueprint, jsonify, render_template, request, send_from_directory
from flask_jwt_extended import current_user as jwt_current_user
from flask_jwt_extended import jwt_required
from flask_login import current_user

from.index import admin_views

from App.controllers import (
    add_student_information,
    update_student
)
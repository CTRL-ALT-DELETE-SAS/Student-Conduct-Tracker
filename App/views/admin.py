import os
from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for, session
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import login_required, login_user, current_user, logout_user
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from.index import index_views

from App.controllers import (
    create_user,
    jwt_authenticate,
    jwt_authenticate_admin,
)

admin_views = Blueprint('admin_views', __name__, template_folder='../templates')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file():
    file = request.files['file']
    if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify({'message': f"File uploaded"}), 200
        
    
@admin_views.route('/students', methods=['POST'])
def add_students():
  token = jwt_authenticate_admin(self.ID, self.password)
  if not token:
     return jsonify({"error": f"Not Authorized"}), 401
  else
    user= User.query.get(current_user.id)
    with open('') as file:
    for row in file:
      id=row['id']
      student=Student.query.get(id) 
      if student:
        flash('error':f"ID already exists {row['id']}"), 400
      elif row['studentType'] != "Full-Time" or row['studentType'] != "Part-Time" or row['studentType'] != "Evening" or or row['studentType'] != "Graduated" or row['studentType'] != "On-Leave"
        flash('error':f"{row['studentType']} was not a valis option"), 400
      else:
       add_student_information(admin=user,id=row['id'],firstname=row['firstname'],lastname=row['lastname'],studentType=row['studentType'],yearofEnrollmentrow=row['yearofEnrollment'])
  flash('database Updated')
  return jsonify({'message': f"Students created"}),200

@admin_views.route('/students', methods=['PUT'])
def update_students():
  return jsonify({'message': f"Students updated"})

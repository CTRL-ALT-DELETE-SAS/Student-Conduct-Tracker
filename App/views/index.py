from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.models import db
from App.controllers import create_admin, create_staff, create_student

index_views = Blueprint('index_views', __name__, template_folder='../templates')

# Define a route for the index view
@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

#Initialize 
@index_views.route('/init', methods=['GET'])
def init():
    db.drop_all()
    db.create_all()
    create_admin('tom', 'white', 'remember')
    create_staff('Jerry', 'Black', 'forgotten', '816084123', 'jerryblack@my.uwi.edu', '10')
    create_student('Bob', 'Gray', 'thinking', '816053863', 'bob.gray@my.uwi.edu', 'Full-time', '2')
    return jsonify(message='db initialized!')

@index_views.route('/test', methods=['GET'])
def health_check():
    return jsonify({'status':'working'})
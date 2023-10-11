import random
from flask import Blueprint, render_template, jsonify
from App.models import db
from App.controllers import create_user, create_staff, create_student
import randomname

index_views = Blueprint('index_views', __name__, template_folder='../templates')

# Define a route for the index view
@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

@index_views.route('/init', methods=['POST'])
def init():
    db.drop_all()
    db.create_all()
    create_user('bob', 'builder', 'bobpass')

    for ID in  range(2, 50): 
        create_staff(
            randomname.get_name(), 
            randomname.get_name(), 
            randomname.get_name(), 
            str(ID), 
            randomname.get_name() + '@schooling.com', 
            str(random.randint(1, 15))
        )
        
    for ID in range(50, 150): 
        create_student(
            randomname.get_name(), 
            randomname.get_name(), 
            randomname.get_name(),
            str(ID),
            randomname.get_name() + '@schooling.com',
            random.choice(['Full-time','Part-time', 'evening']),
            str(random.randint(1, 8))
        )

    return jsonify(message='db initialized!')
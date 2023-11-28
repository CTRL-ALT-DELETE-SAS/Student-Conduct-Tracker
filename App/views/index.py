import random
from flask import Blueprint, render_template, jsonify
from App.models import db
from App.controllers import *
import randomname


index_views = Blueprint('index_views', __name__, template_folder='../templates')

# Define a route for the index view
@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

def generate_random_contact_number():
    return f"0000-{random.randint(100, 999)}-{random.randint(1000, 9999)}"


@index_views.route('/init', methods=['POST'])
def init():
    db.drop_all()
    db.create_all()
    admin= create_admin('bob', 'boblast' , 'bobpass')
      
    staff = create_staff(admin, '0012', 'John', 'Mann,' 'johnpass', 'johnmann@schooling.com')
    staff = create_staff(admin, '0013', 'Jane', 'Anne,' 'janepass', 'janeanne@schooling.com')

    student = create_student(admin, '0021', 'Nick', 'Dell', generate_random_contact_number(), random.choice(['Full-Time','Part-Time', 'Evening']), str(random.randint(1, 8)))
    student = create_student(admin, '0022', 'John', 'Biz', generate_random_contact_number(), random.choice(['Full-Time','Part-Time', 'Evening']), str(random.randint(1, 8)))
    

    return jsonify({'message': 'Database initialized'}),201
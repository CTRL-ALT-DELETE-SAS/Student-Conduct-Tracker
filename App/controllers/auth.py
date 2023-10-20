from functools import wraps
from flask_login import current_user, LoginManager, login_user
from flask_jwt import JWT
from App.database import db
from flask_jwt_extended import create_access_token, jwt_required, JWTManager

from App.models import Staff, Student, Admin


def jwt_authenticate(id, password):
     
	staff = db.session.query(Staff).filter_by(ID=id).first()
	if staff and staff.check_password(password):
		return create_access_token(identity=id)
     
	student = db.session.query(Student).filter_by(ID=id).first()
	if student and student.check_password(password):
		return create_access_token(identity=id)
     
	admin = db.session.query(Admin).filter_by(ID=id).first()
	if admin and admin.check_password(password):
			return create_access_token(identity=id)
	return None


def login(id, password):    

    staff = db.session.query(Staff).filter_by(ID=id).first()
    if staff and staff.check_password(password):
        login_user(staff)
        return staff
   
    student = db.session.query(Student).filter_by(ID=id).first()
    if student and student.check_password(password):
        login_user(student)
        return student

    admin = db.session.query(Admin).filter_by(ID=id).first()
    if admin and admin.check_password(password):
        login_user(admin)
        return admin
    
    return None


def setup_flask_login(app):
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        if Staff.query.get(user_id) is Staff: 
            return Staff.query.get(user_id)
        if Student.query.get(user_id) is Student: 
            return Student.query.get(user_id)
        if Admin.query.get(user_id) is Admin: 
            return Admin.query.get(user_id)

    return login_manager


def setup_jwt(app):
    jwt = JWTManager(app)

    @jwt.user_identity_loader
    def user_identity_lookup(identity):
        if Staff.query.filter_by(ID=identity).one_or_none() is Staff:
            return Staff.query.filter_by(ID=identity).one_or_none().ID
        if Admin.query.filter_by(ID=identity).one_or_none() is Admin:
            return Admin.query.filter_by(ID=identity).one_or_none().ID
        if Student.query.filter_by(ID=identity).one_or_none() is Student:
            return Student.query.filter_by(ID=identity).one_or_none().ID

        return None
 

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        if Staff.query.get(identity) is Staff: 
            return Staff.query.get(identity)
        if Admin.query.get(identity) is Admin: 
            return Admin.query.get(identity)
        if Student.query.get(identity) is Student: 
            return Student.query.get(identity)

    return jwt


def student_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not isinstance(current_user, Student):
            return "Unauthorized", 401
        return func(*args, **kwargs)
    return wrapper


def staff_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not isinstance(current_user, Staff):
            return "Unauthorized", 401
        return func(*args, **kwargs)
    return wrapper


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not isinstance(current_user, Admin):
            return "Unauthorized", 401
        return func(*args, **kwargs)
    return wrapper

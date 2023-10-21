from functools import wraps
from flask_login import current_user, LoginManager, login_user
from App.database import db
from flask_jwt_extended import create_access_token, jwt_required, JWTManager

from App.models import Staff, Student, Admin, User


def jwt_authenticate(id, password):
	staff = Staff.query.filter_by(ID=id).first()
	if staff and staff.check_password(password):
		return create_access_token(identity=id)
     
	student = Student.query.filter_by(ID=id).first()
	if student and student.check_password(password):
		return create_access_token(identity=id)
     
	admin = Admin.query.filter_by(ID=id).first()
	if admin and admin.check_password(password):
			return create_access_token(identity=id)
		
	return None


def login(id, password):    

    staff = Staff.query.filter_by(ID=id).first()
    if staff and staff.check_password(password):
        return staff
   
    student = Student.query.filter_by(ID=id).first()
    if student and student.check_password(password):
        return student

    admin = Admin.query.filter_by(ID=id).first()
    if admin and admin.check_password(password):
        return admin
    return None


def setup_flask_login(app):
	login_manager = LoginManager()
	login_manager.init_app(app)
	
	@login_manager.user_loader
	def load_user(user_id):
		staff = Staff.query.get(user_id)
		if staff:
			return staff

		student = Student.query.get(user_id)
		if student:
			return student

		admin = Admin.query.get(user_id)
		if admin:
			return admin
		return login_manager


def setup_jwt(app):
		jwt = JWTManager(app)
	
		@jwt.user_identity_loader
		def user_identity_lookup(identity):
			staff= Staff.query.filter_by(ID=identity).one_or_none()
			if staff:
				return staff.ID
			
			admin= Admin.query.filter_by(ID=identity).one_or_none()
			if admin:
				return admin.ID
      
			student= Student.query.filter_by(ID=identity).one_or_none() 
			if student:
				return student.ID

			return None
 

		@jwt.user_lookup_loader
		def user_lookup_callback(_jwt_header, jwt_data):
				identity = jwt_data["sub"]
				staff = Staff.query.get(identity)
				if staff:
						return staff
		
				student = Student.query.get(identity)
				if student:
						return student
		
				admin = Admin.query.get(identity)
				if admin:
						return admin
		
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

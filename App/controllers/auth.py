from functools import wraps
from flask_login import current_user, LoginManager
from flask_jwt import JWT
from App.database import db
from flask_jwt_extended import create_access_token, jwt_required, JWTManager

from App.models import User, Staff, Student, Admin


def authenticate(firstname, lastname, password):
    staff = db.session.query(Staff).filter_by(
        firstname=firstname, lastname=lastname).first()
    if staff and staff.check_password(password):
        return staff
    student = db.session.query(Student).filter_by(
        firstname=firstname, lastname=lastname).first()
    if student and student.check_password(password):
        return student
    admin = db.session.query(Admin).filter_by(
        firstname=firstname, lastname=lastname).first()
    if admin and admin.check_password(password):
        return admin
    return None

def jwt_authenticate(id, password):
	staff = db.session.query(Staff).filter_by(
			ID=id).first()
	if staff and staff.check_password(password):
			return create_access_token(identity=id)
	student = db.session.query(Student).filter_by(
	ID=id).first()
	if student and student.check_password(password):
			return create_access_token(identity=id)
	admin = db.session.query(Admin).filter_by(
	ID=id).first()
	if admin and admin.check_password(password):
			return create_access_token(identity=id)
	return None

def identity(payload):
    staff = db.session.query(Staff).get(payload['identity'])
    if staff:
        return staff
    student = db.session.query(Student).get(payload['identity'])
    if student:
        return student
    admin = db.session.query(Admin).get(payload['identity'])
    if admin:
        return admin
    return None


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


def setup_flask_login(app):
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)

    return login_manager


def setup_jwt(app):
    return JWT(app, authenticate, identity)


def user_identity_lookup(identity):
    user = db.session.query(User).filter_by(id=identity).one_or_none()
    if user:
        return user.id
    return None


def user_lookup_callback(_jwt_header, jwt_data):
    identification = jwt_data["sub"]
    return str(identification)

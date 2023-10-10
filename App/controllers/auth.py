from functools import wraps
from flask_login import current_user, LoginManager
from flask_jwt import JWT

from App.models import User, Staff, Student, Admin


def authenticate(firstname, lastname, password):
    staff = Staff.query.filter_by(
        firstname=firstname, lastname=lastname).first()
    if staff and staff.check_password(password):
        return staff
    student = Student.query.filter_by(
        firstname=firstname, lastname=lastname).first()
    if student and student.check_password(password):
        return student
    admin = Admin.query.filter_by(
        firstname=firstname, lastname=lastname).first()
    if Admin and admin.check_password(password):
        return admin
    return None


def identity(payload):
    staff = Staff.query.get(payload['identity'])
    if staff:
        return staff
    student = Student.query.get(payload['identity'])
    if student:
        return student
    admin = Admin.query.get(payload['identity'])
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
        return User.query.get(user_id)

    return login_manager


def setup_jwt(app):
    return JWT(app, authenticate, identity)


def user_identity_lookup(identity):
    user = User.query.filter_by(id=identity).one_or_none()
    if user:
        return user.id
    return None


def user_lookup_callback(_jwt_header, jwt_data):
    identification = jwt_data["sub"]
    return User.query.get(identification)

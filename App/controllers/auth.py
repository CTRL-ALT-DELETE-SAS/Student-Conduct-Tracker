from flask_login import login_user, login_manager, logout_user, LoginManager
from flask_jwt_extended import create_access_token, jwt_required, JWTManager

from App.models import db, User, Staff,Student, Admin, 

def jwt_authenticate(username, password):
  user = User.query.filter_by(username=username).first()
  if user and user.check_password(password):
    return create_access_token(identity=username)
  return None

def login_staff(password, staffID):
    staff = Staff.query.filter_by(staffID= staffID).first()
    if staff and staff.check_password(password):
        login_user(staff)
        return staff
    return None

def login_student(password, studentID):
    student = Student.query.filter_by(studentID= studentID).first()
    if student and student.check_password(password):
        login_user(student)
        return student
    return None
  
  def login_admin(password, staffID):
    admin = Admin.query.filter_by(staffID= staffID).first()
    if admin and admin.check_password(password):
        login_user(admin)
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

  def get_all_students_json():
    students = Student.query.all()
    if not student:
      return []
    students= [student.toDict() for student in students]
    return students

  def get_all_staff_json():
    staffmembers = Staff.query.all()
    if not staff:
      return []
    staffmembers= [staff.toDict() for staff in staffmembers]
    return staffmembers

  def get_all_students():
    return Student.query.all()

  def get_all_staff():
    return Staff.query.all()

def setup_flask_login(app):
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
    
    return login_manager

def setup_jwt(app):
    jwt = JWTManager(app)

    @jwt.user_identity_loader
    def user_identity_lookup(identity):
        user = User.query.filter_by(username=identity).one_or_none()
        if user:
            return user.id
        return None

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.get(identity)

    return jwt

from functools import wraps
from flask_login import current_user, LoginManager, login_user
from App.database import db
from flask_jwt_extended import create_access_token, jwt_required, JWTManager

from App.models import Staff, Admin, User


def jwt_authenticate(id, password):
  staff = Staff.query.filter_by(id=id).first()
  if staff and staff.check_password(password):
    return create_access_token(identity=id)
  return None

def jwt_authenticate_admin(id, password):
  admin = Admin.query.filter_by(id=id).first()
  if admin and admin.check_password(password):
    return create_access_token(identity=id)

  return None


def login(id, password):    

    staff = Staff.query.filter_by(id=id).first()
    if staff and staff.check_password(password):
        return staff

    admin = Admin.query.filter_by(id=id).first()
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

    admin = Admin.query.get(user_id)
    if admin:
      return admin
    return login_manager


def setup_jwt(app):
  jwt = JWTManager(app)

  @jwt.user_identity_loader
  def user_identity_lookup(identity):
    admin = Admin.query.filter_by(id=identity).one_or_none()
    if admin:
      return admin.id

    staff = Staff.query.filter_by(id=identity).one_or_none()
    if staff:
      return staff.id

    return None


  @jwt.user_lookup_loader
  def user_lookup_callback(_jwt_header, jwt_data):
      identity = jwt_data["sub"]

      admin = Admin.query.filter_by(id=identity).one_or_none()
      if admin:
          return admin

      staff = Staff.query.filter_by(id=identity).one_or_none()
      if staff:
          return staff
  return jwt


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

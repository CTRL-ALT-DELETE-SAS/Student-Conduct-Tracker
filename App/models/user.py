from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from App.database import db
from abc import ABC


class User(db.Model, UserMixin):
  __abstract__ = True

  firstname = db.Column(db.String(120), nullable=False)
  lastname = db.Column(db.String(120), nullable=False)
  password = db.Column(db.String(120), nullable=False)

  def __init__(self, firstname, lastname, password):
    self.firstname = firstname
    self.lastname = lastname
    self.set_password(password)

  def to_json(self):
    return {
      'firstname': self.firstname, 
      'lastname': self.lastname
    }

  def set_password(self, password):
    """Create hashed password."""
    self.password = generate_password_hash(password, method='sha256')

  def check_password(self, password):
    """Check hashed password."""
    return check_password_hash(self.password, password)
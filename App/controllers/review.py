from App.models import Review, Staff, Student
from App.database import db

def get_reviews_by_student(studentID):
  return Review.query.filter_by(studentID=studentID).all()

def get_reviews_by_staff(staffID):
  return Review.query.filter_by(staffID=staffID).all()

def editReview(self, staff, isPositive, comment):
    if self.reviewer == staff:
      self.isPositive = isPositive
      self.comment = comment
      db.session.add(self)
      db.session.commit()
      return True
    return None

  def deleteReview(self, staff):
    if self.reviewer == staff:
      db.session.delete(self)
      db.session.commit()
      return True
    return None
    

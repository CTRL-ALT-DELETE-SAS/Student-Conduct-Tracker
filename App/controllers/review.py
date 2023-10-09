from App.models import Review, Staff, Student
from App.database import db

def get_reviews_by_student(studentID):
  return Review.query.filter_by(studentID=studentID).all()

def get_reviews_by_staff(staffID):
  return Review.query.filter_by(staffID=staffID).all()

def delete_review(staffID, reviewID):
  staff= Staff.query.get(staffID)
  review = Review.query.get(reviewID)
  if review and staff:
    return staff.delete_review(review)
  return False

def edit_review(staffID, reviewID):
  staff= Staff.query.get(staffID)
  review = Review.query.get(reviewID)
  if review and staff:
    

from App.database import db
from App.models import Staff, Review, Admin
from App.controllers import *


def create_review(staffID, studentID, isPositive, comment):
  staff = get_staff(staffID)
  student = get_student(studentID)
  review = staff.createReview(student, isPositive, comment)
  if review:
      return review
  return False

def searchStudents(staff, search_query):
  students = staff.searchStudent(search_query)
  return students
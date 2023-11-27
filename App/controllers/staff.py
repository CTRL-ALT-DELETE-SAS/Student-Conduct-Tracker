from App.database import db
from App.models import Staff, Review, Admin


def create_review(staffID, studentID, isPositive, comment):
  staff = get_staff(staffID)
  review = staff.createReview(studentID, isPositive, comment)
  if review:
      return review
  return False

def search_students_searchTerm(staff, searchTerm):
  students = staff.searchStudent(searchTerm)
  if students:
    return students
  return None
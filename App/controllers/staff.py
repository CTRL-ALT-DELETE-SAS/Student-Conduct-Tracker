from App.controllers.user import get_staff
from App.models import Staff, Student, Review, Karma
from App.database import db

def create_review(staffID, studentID, is_positive, comment):
    staff = get_staff(staffID)
    student = db.session.query(Student).get(studentID)
    
    if staff and student:
        review = staff.createReview(student,is_positive, comment)
        return review
    return None

def search_students_searchTerm(staff, searchTerm):
    students = staff.searchStudent(searchTerm)
    if students:
      return students
    return None
from App.models import Staff, Student, Review
from App.database import db

def create_review(staffID, studentID, is_positive, comment):
    staff = get_staff_by_id(staffID)
    student = db.session.query(Student).get(studentID)
    
    if staff and student:
        review = Review(reviewer=staff, student=student, isPositive=is_positive, comment=comment)
        db.session.add(review)
        db.session.commit()
        return review
    return None

def get_staff_by_id(staff_id):
    return  db.session.query(Staff).get(staff_id)

def get_staff_reviews(staff_id):
    staff = get_staff_by_id(staff_id)
    if staff:
        return staff.getReviewsByStaff(staff)

def search_students_searchTerm(searchTerm):
    staff = Staff().searchStudent(searchTerm)
    return staff

def get_student_rankings():
    staff = Staff()
    return staff.getStudentRankings()
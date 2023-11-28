from App.controllers.user import get_staff
from App.models import Staff

def create_review(staffID, studentID, is_positive, comment):
    staff = get_staff(staffID)
    return staff.createReview(studentID, is_positive, comment)

def get_staff_reviews(staff_id):
    staff = get_staff(staff_id)
    return staff.getReviewsByStaff(staff)

def search_students_searchTerm(staff, searchTerm):
    return staff.searchStudent(searchTerm)
  
def get_student_rankings(staff):
    return staff.getStudentRankings()
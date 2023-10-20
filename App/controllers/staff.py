from App.controllers.user import get_staff
from App.models import Staff, Student, Review, Karma
from App.database import db

def create_review(staffID, studentID, is_positive, comment):
    staff = get_staff(staffID)
    student = db.session.query(Student).get(studentID)
    
    if staff and student:
        review = Review(reviewer=staff, student=student, isPositive=is_positive, comment=comment)
        db.session.add(review)
        db.session.commit()
        return review
    return None

def get_staff_reviews(staff_id):
    staff = get_staff(staff_id)
    if staff:
        return staff.getReviewsByStaff(staff)

def search_students_searchTerm(searchTerm):
    students = searchStudent(searchTerm)
    return students

def get_student_rankings():
    staff = Staff()
    return staff.getStudentRankings()

def searchStudent(searchTerm):
    # Query the Student model for a student by ID or first name, or last name
    students = db.session.query(Student).filter(
        (Student.ID == searchTerm)
        |  #studentID must be exact match (string)
        (Student.firstname.ilike(f"%{searchTerm}%"))
        |  # Search by firstname or lastname - case-insensitive
        (Student.lastname.ilike(f"%{searchTerm}%"))).all()

    if students:
      # If matching students are found, return their json representations in a list
      return [student.to_json() for student in students]
    else:
      # If no matching students are found, return an empty list
      return []
    
def getStudentRankings():
    students = db.session.query(Student, Karma)\
                .join(Karma, Student.karmaID == Karma.karmaID)\
                .order_by(Karma.rank.asc())\
                .all()

    if students:
      # If students with rankings are found, return a list of their JSON representations
      student_rankings = [{
          "studentID": student.Student.ID,
          "firstname": student.Student.firstname,
          "lastname": student.Student.lastname,
          "karmaScore": student.Karma.score,
          "karmaRank": student.Karma.rank
      } for student in students]
      return student_rankings
    else:
      # If no students with rankings are found, return an empty list
      return []


from App.database import db
from .user import User
from .student import Student
from .karma import Karma
from .review import Review


class Staff(User):
  __tablename__ = 'staff'
  ID = db.Column(db.String(10), primary_key=True)
  email = db.Column(db.String(120), nullable=False)
  teachingExperience = db.Column(db.Integer, nullable=False)

  def __init__(self, staffID, firstname, lastname, password, email,
               teachingExperience):
    super().__init__(firstname, lastname, password)
    self.ID = staffID
    self.email = email
    self.teachingExperience = teachingExperience

  def get_id(self):
    return self.ID

#return staff details on json format

  def to_json(self):
    return {
        "staffID": self.ID,
        "firstname": self.firstname,
        "lastname": self.lastname,
        "email": self.email,
        "teachingExperience": self.teachingExperience
    }

# Retrieve reviews by a staff member from the Review model

  def getReviewsByStaff(self, staff):
    staff_reviews = staff.reviews_created
    return [review.to_json() for review in staff_reviews]

#create a review for a student

  def createReview(self, student, isPositive, comment):
    review = Review(self, student, isPositive, comment)
    student.reviews.append(review)  #add review to the student
    db.session.add(review)  #add to db
    db.session.commit()
    return review

  def searchReview(self, search_term):
        staff_reviews = self.reviews_created
        filtered_reviews = [review for review in staff_reviews if search_term.lower() in review.comment.lower()]
        return filtered_reviews

  def searchStudent(self, searchTerm):
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


#get student karma rankings from highest rank to lowest based on scores

  def getStudentRankings(self):
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

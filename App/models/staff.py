from App.database import db
from .user import User
from .student import Student
from .karma import Karma
from .review import Review


class Staff(User):
  __tablename__ = 'staff'
  id = db.Column(db.String(10), primary_key=True)
  email = db.Column(db.String(120), nullable=False)

  def __init__(self, id, firstname, lastname, password, email,):
    super().__init__(firstname, lastname, password)
    self.id = id
    self.email = email

  def createReview(self, student, isPositive, comment):
    review = Review(self, student, isPositive, comment)
    student.reviews.append(review)  
    try:
      db.session.add(review)  
      db.session.commit()
      return review
    except:
      return False

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
  
  #return staff details on json format
  def to_json(self):
    return {
        "id": self.id,
        "firstname": self.firstname,
        "lastname": self.lastname,
        "email": self.email
    }
from App.database import db
from .student import Student
from .karma import Karma
from .staff import Staff
from .user import User

class Admin(User):
	id = db.Column(db.String, primary_key= True)

	def __init__(self, firstname, lastname, password):
		super().__init__(firstname, lastname, password)
		self.id = "A" + str(Admin.query.count() + 1)

	def addStudent(self, id, firstname, lastname, contact, studentType, yearofStudy):
		newKarma = Karma()
		try:
			db.session.add(newKarma)
			db.session.commit()
		except:
			db.session.rollback()
			return False


		newStudent= Student(id, firstname, lastname, contact, studentType, yearofStudy)
		
		newStudent.karmaID = newKarma.karmaID
		newKarma.studentID = newStudent.id
		try:
			db.session.add(newStudent)
			db.session.commit()
			return newStudent
		except:
			db.session.rollback()
			return False


	def addStaff(self, id, firstname, lastname, password, email):
		newStaff= Staff(id, firstname, lastname, password, email)	
		try:
			db.session.add(newStaff)
			db.session.commit()
			return newStaff
		except:
			return False
	
	def updateStudent(self, student, firstname, lastname, contact, studentType, yearofStudy):
		student.firstname = firstname
		student.lastname = lastname
		student.contact = contact
		student.studentType = studentType
		student.yearOfStudy = yearofStudy
		try:
			db.session.add(student)
			db.session.commit()
			return True
		except:
			db.session.rollback()
			return False
		return False
	
	def to_json(self):
		return {
	        "id": self.id,
    	    "firstname": self.firstname,
        	"lastname": self.lastname
    	}
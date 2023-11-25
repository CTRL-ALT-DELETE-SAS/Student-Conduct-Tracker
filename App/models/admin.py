from App.database import db
from .student import Student
from .staff import Staff
from .user import User

class Admin(User):
	id = db.Column(db.String, primary_key= True)

	def __init__(self, firstname, lastname, password):
		super().__init__(firstname, lastname, password)
		self.id = "A" + str(Admin.query.count() + 1)

	def addStudent(self, id, firstname, lastname, contact, studentType, yearofStudy):
		newStudent= Student(id, firstname, lastname, contact, studentType, yearofStudy)
		try:
			db.session.add(newStudent)
			db.session.commit()
			return newStudent
		except:
			return False


	def addStaff(self, id, firstname, lastname, password, email):
		newStaff= Staff(id, firstname, lastname, password, email)	
		try:
			db.session.add(newStaff)
			db.session.commit()
			return newStaff
		except:
			return False
	
	def updateStudent(self, studentID, field_to_update, new_value):
		allowed_fields = ["id", "firstname", "lastname", "contact", "studenttype", "yearofstudy"]
		input_field = field_to_update.lower().replace('-', '').replace('_', '').replace(' ', '')

		student = Student.query.filter_by(id=studentID).first()

		if student is None:
			return "Student not found"

		found_field = None
		for field in Student.__table__.columns.keys():
			if field.lower() == input_field:
				found_field = field
				break

		if found_field is None:
			return f"Field '{field_to_update}' does not exist for Student"

		# Check if the specified field is in the list of editable fields
		if input_field not in allowed_fields:
			return f"Field '{field_to_update}' cannot be updated for Student"

		# Update the specified field with the new value
		setattr(student, found_field, new_value)

		# Commit to save the changes
		db.session.add(student)
		db.session.commit()
		return True
	
	def to_json(self):
		return {
	        "id": self.id,
    	    "firstname": self.firstname,
        	"lastname": self.lastname
    	}

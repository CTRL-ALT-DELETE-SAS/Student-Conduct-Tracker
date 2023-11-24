from datetime import datetime
from App.database import db

class Student(db.Model):
	__tablename__ = 'student'
	ID = db.Column(db.String(10), primary_key=True)
	firstname = db.Column(db.String(120), nullable=False)
	lastname = db.Column(db.String(120), nullable=False)
	studentType = db.Column(db.String(30))  #full-time, part-time or evening
	yearOfEnrollment = db.Column(db.Integer)
	reviews = db.relationship('Review', backref='student', lazy='joined')
	karmaID = db.Column(db.Integer, db.ForeignKey('karma.karmaID'))

  #When student is newly created there would be no reviews or karma yet
	def __init__(self, studentID, firstname, lastname, studentType, yearofEnrollment):
		self.ID = studentID
		self.firstname = firstname
		self.lastname = lastname
		self.studentType = studentType
		self.yearOfEnrollment = yearofEnrollment
		self.reviews = []
	
	def get_id(self):
		return self.ID

#Gets the student details and returns in JSON format
	def to_json(self):
		karma = self.getKarma()
		return {
        "studentID": self.ID,
        "firstname": self.firstname,
        "lastname": self.lastname,
        "studentType": self.studentType,
		"yearOfEnrollment": self.yearOfEnrollment,
        "yearOfStudy": (datetime.now().year) - self.yearOfEnrollment, #Dynamically calculate year based on enrollment date
        "reviews": [review.to_json() for review in self.reviews],
		"karmaScore": karma.score if karma else None,
        "karmaRank": karma.rank if karma else None,
    }

#get karma record from the karma table using the karmaID attached to the student
	def getKarma(self):
		from .karma import Karma
		return Karma.query.get(self.karmaID)

from App.database import db
from .user import User
from .karma import Karma


class Student():
	__tablename__ = 'student'
	ID = db.Column(db.String(10), primary_key=True)
	contact = db.Column(db.String(30), nullable=False)
	studentType = db.Column(db.String(30))  #full-time, part-time or evening
	yearOfStudy = db.Column(db.Integer, nullable=False)
	reviews = db.relationship('Review', backref='student', lazy='joined')
	karmaID = db.Column(db.Integer, db.ForeignKey('karma.karmaID'))

	def __init__(self, studentID, firstname, lastname, password, contact, studentType, yearofStudy):
		super().__init__(firstname, lastname, password)
		self.ID = studentID
		self.contact = contact
		self.studentType = studentType
		self.yearOfStudy = yearofStudy
		self.reviews = []
		newKarma = Karma()
		self.karmaID = newKarma.karmaID

	def to_json(self):
		karma = self.getKarma()
		return {
			"studentID": self.ID,
			"firstname": self.firstname,
			"lastname": self.lastname,
			"contact": self.contact,
			"studentType": self.studentType,
			"yearOfStudy": self.yearOfStudy,
			"reviews": [review.to_json() for review in self.reviews],
					"karmaScore": karma.score if karma else None,
			"karmaRank": karma.rank if karma else None,
    	}

	def updateKarma(self):
		karma = Karma.query.get(self.karmaID)
		karma.calculateScore(self)
from App.database import db
from .karma import Karma


class Student(db.Model):
	__tablename__ = 'student'
	id = db.Column(db.String(10), primary_key=True)
	firstname = db.Column(db.String(120), nullable=False)
	lastname = db.Column(db.String(120), nullable=False)
	contact = db.Column(db.String(30), nullable=False)
	studentType = db.Column(db.String(30))  #full-time, part-time or evening
	yearOfStudy = db.Column(db.Integer, nullable=False)
	reviews = db.relationship('Review', backref='student', lazy='joined')
	karmaID = db.Column(db.Integer, db.ForeignKey('karma.karmaID', use_alter=True))

	def __init__(self, id, firstname, lastname, contact, studentType, yearofStudy):
		self.id = id
		self.firstname = firstname
		self.lastname = lastname
		self.contact = contact
		self.studentType = studentType
		self.yearOfStudy = yearofStudy
		self.reviews = []

	def updateKarma(self):
		karma = Karma.query.get(self.karmaID)
		score = karma.calculateScore(self)
		if score:
			if Karma.updateRank():
				return True
			return False
		return False
		
		
	def to_json(self):
		karma = Karma.query.get(self.karmaID)
		return {
			"id": self.id,
			"firstname": self.firstname,
			"lastname": self.lastname,
			"contact": self.contact,
			"studentType": self.studentType,
			"yearOfStudy": self.yearOfStudy,
			"karmaScore" : karma.score,
			"karmaRank" : karma.rank
    	}
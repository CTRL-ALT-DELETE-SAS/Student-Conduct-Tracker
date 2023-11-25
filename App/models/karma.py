from App.database import db
from .student import Student


class Karma(db.Model):
  __tablename__ = "karma"
  karmaID = db.Column(db.Integer, primary_key=True)
  score = db.Column(db.Float, nullable=False, default=0.0)
  studentID = db.Column(db.String(10), db.ForeignKey('student.id'))


  def __init__(self, score=0.0):
    self.score = score

  # calculate the karma score for the provided student based on reviews
  def calculateScore(self, student):
    goodKarma = 0
    badKarma = 0

    for review in student.reviews:
      if review.isPositive == True:  
        goodKarma += review.upvotes
        badKarma += review.downvotes
      else:  
        badKarma += review.upvotes
        goodKarma += review.downvotes

    self.score = goodKarma - badKarma

    try:
      db.session.add(self)
      db.session.commit()
      return True
    except:
      db.session.rollback()
      return False
  
  # retrieves karma score
  def getScore(self):
    return self.score

  def to_json(self):
    return {
      "karmaID": self.karmaID, 
      "score": self.score,
      "studentID" : self.studentID
    }
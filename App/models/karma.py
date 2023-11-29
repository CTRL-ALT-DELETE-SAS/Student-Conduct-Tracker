from App.database import db
from App.models import *


class Karma(db.Model):
  __tablename__ = "karma"
  karmaID = db.Column(db.Integer, primary_key=True)
  score = db.Column(db.Float, nullable=False, default=0.0)
  rank = db.Column(db.Integer, nullable=False, default=-99)
  studentID = db.Column(db.String(10), db.ForeignKey('student.id', use_alter=True))

  def __init__(self, score=0.0, rank=-99):
    self.score = score
    self.rank = rank

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

  @classmethod
  def updateRank(cls):
    # Calculate the rank of students based on their karma score
    # Query all students with karma scores in descending order
    
    studentsOrdered = db.session.query(Student, Karma)\
               .join(Karma, Student.karmaID == Karma.karmaID)\
               .order_by(db.desc(Karma.score))\
               .all()

    rank = 1
    prev_score = None

    #assign ranks to student with the highest karma at the top
    for student, karma in studentsOrdered:
      if prev_score is None:
        prev_score = karma.score
        karma.rank = rank
      elif prev_score == karma.score:
        karma.rank = rank
      else:
        rank += 1
        karma.rank = rank
        prev_score = karma.score

  # Commit the changes to the database
    try:
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
from App.database import db
from .student import Student


class Karma(db.Model):
  __tablename__ = "karma"
  karmaID = db.Column(db.Integer, primary_key=True)
  score = db.Column(db.Float, nullable=False, default=0.0)


  def __init__(self, score=0.0):
    self.score = score

  def to_json(self):
    return {"karmaID": self.karmaID, "score": self.score}

  # Calculate the karma score for the provided student based on reviews
  def calculateScore(self, student):
    goodKarma = 0
    badKarma = 0

    for review in student.reviews:
      if review.isPositive == True:  #if review is positive then upvotes on the review contributes to good karma
        goodKarma += review.upvotes
        badKarma += review.downvotes
      else:  #if review is not positive then upvotes on the review contributes to bad karma
        badKarma += review.upvotes
        goodKarma += review.downvotes

    self.score = goodKarma - badKarma
    #student.karmaID = self.karmaID

    try:
      db.session.add(self)
      db.session.commit()
      return True

    except:
      db.session.rollback()
      return False
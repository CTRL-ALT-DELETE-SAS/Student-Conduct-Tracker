from App.models import Karma, Student
from App.database import db

def get_karma_by_id(karma_id):
    return db.session.query(Karma).get(karma_id)

def calculate_student_karma(student):
    good_karma = 0
    bad_karma = 0

    for review in student.reviews:
        if review.isPositive:
            good_karma += review.upvotes
            bad_karma += review.downvotes
        else:
            bad_karma += review.upvotes
            good_karma += review.downvotes

    karma_score = good_karma - bad_karma

    if student.karmaID is not None:
        karma = db.session.query(Karma).get(student.karmaID)
        karma.score = karma_score
    else:
        karma = Karma(score=karma_score)
        db.session.add(karma)
        db.session.flush() 
        student.karmaID = karma.karmaID

    db.session.commit()
    return karma

def update_student_karma_rankings():
    students_with_karma = db.session.query(Student, Karma)\
        .join(Karma, Student.karmaID == Karma.karmaID)\
        .order_by(db.desc(Karma.score))\
        .all()

    rank = 1
    prev_score = None

    for student, karma in students_with_karma:
        if prev_score is None:
            prev_score = karma.score
            karma.rank = rank
        elif prev_score == karma.score:
            karma.rank = rank
        else:
            rank += 1
            karma.rank = rank
            prev_score = karma.score

        student.karmaID = karma.karmaID
    db.session.commit()
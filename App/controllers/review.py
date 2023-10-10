from App.models import Review, Staff, Student
from App.database import db


def get_reviews_by_student(studentID):
    return Review.query.filter_by(studentID=studentID).all()


def get_reviews_by_staff(staffID):
    return Review.query.filter_by(reviewerID=staffID).all()


def edit_review(review, staff, is_positive, comment):
    if review.reviewer == staff:
        review.isPositive = is_positive
        review.comment = comment
        db.session.add(review)
        db.session.commit()
        return True
    return None


def delete_review(review, staff):
    if review.reviewer == staff:
        db.session.delete(review)
        db.session.commit()
        return True
    return None

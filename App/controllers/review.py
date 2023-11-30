from App.models import Review, Karma, Student
from App.database import db

def get_reviews(): 
    return db.session.query(Review).all()

def get_reviews_for_student(studentID):
    return db.session.query(Review).filter_by(studentID=studentID).all()

def get_review(reviewID):
    return Review.query.filter_by(ID=reviewID).first()

def get_reviews_by_staff(staffID):
    return db.session.query(Review).filter_by(reviewerID=staffID).all()

def edit_review(review, staff, is_positive, comment):
    edit = review.editReview(staff, is_positive, comment)
    if edit:
        return review
    return None

def delete_review(review, staff):
    return review.deleteReview(staff)

def downvote(reviewID, staff):
    review = get_review(reviewID)
    return review.downvoteReview(staff)


def upvote(reviewID, staff):
    review = get_review(reviewID)
    return review.upvoteReview(staff)
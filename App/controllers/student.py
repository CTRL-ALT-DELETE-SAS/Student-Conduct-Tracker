from App.models import Student
from App.database import db


def search_student(studentID):
    student = db.session.query(Student).get(studentID)
    if student:
        return student
    return f'{studentID} not found'

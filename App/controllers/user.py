from App.models import User, Staff, Student, Admin
from App.database import db


def create_student(firstname, lastname, password, id, contact, studentType, yearofStudy):
    new_student = Student(firstname=firstname, lastname=lastname, password=password,
                          id=id, contact=contact, studentType=studentType, yearofStudy=yearofStudy)
    db.session.add(new_student)
    db.session.commit()
    return new_student


def create_staff(firstname, lastname, password, id, email, teachingExperience):
    new_staff = Staff(firstname=firstname, lastname=lastname, password=password,
                      id=id, email=email, teachingExperience=teachingExperience)
    db.session.add(new_staff)
    db.session.commit()
    return new_staff


def create_user(firstname, lastname, password):
    new_admin = Admin(firstname=firstname,
                      lastname=lastname, password=password)
    db.session.add(new_admin)
    db.session.commit()
    return new_admin


def get_staff(id):
    return Staff.query.get(id)


def get_student(id):
    return Student.query.get(id)


def is_staff(id):
    return Staff.query.get(id) is not None


def is_student(id):
    return Student.query.get(id) is not None


def is_admin(id):
    return Admin.query.get(id) is not None

def get_all_users_json():
    users = User.query.all()
    users = [user.to_json() for user in users]
    return users

def get_all_students_json():
    students = Student.query.all()
    if not students:
        return []
    students = [student.to_json() for student in students]
    return students


def get_all_staff_json():
    staff_members = Staff.query.all()
    if not staff_members:
        return []
    staff_members = [staff.to_json() for staff in staff_members]
    return staff_members

def get_all_users():
    return User.query.all()

def get_all_students():
    return Student.query.all()


def get_all_staff():
    return Staff.query.all()


def update_student(id, contact, studentType, yearofStudy):
    student = get_student(id)
    if student:
        student.contact = contact
        student.studentType = studentType
        student.yearofStudy = yearofStudy
        db.session.add(student)
        db.session.commit()
        return student
    return None

from App.models import Staff, Student, Admin
from App.database import db


def create_student(firstname, lastname, password, studentID, contact, studentType, yearofStudy):
    new_student = Student(firstname=firstname, lastname=lastname, password=password,
                          studentID=studentID, contact=contact, studentType=studentType, yearofStudy=yearofStudy)
    db.session.add(new_student)
    db.session.commit()
    return new_student


def create_staff(firstname, lastname, password, staffID, email, teachingExperience):
    new_staff = Staff(firstname=firstname, lastname=lastname, password=password,
                      staffID=staffID, email=email, teachingExperience=teachingExperience)
    db.session.add(new_staff)
    db.session.commit()
    return new_staff


def create_user(firstname, lastname, password):
    new_admin = Admin(firstname=firstname, lastname=lastname, password=password)
    db.session.add(new_admin)
    db.session.commit()
    return new_admin


def get_staff(id):
    return db.session.query(Staff).get(id)


def get_student(id):
    return db.session.query(Student).get(id)


def is_staff(id):
    return db.session.query(Staff).get(id) is not None


def is_student(id):
    return db.session.query(Student).get(id) is not None


def is_admin(id):
    return db.session.query(Admin).get(id) is not None 

def get_all_users_json():
    users = get_all_users()
    if not users:
        return []
    users = [user.to_json() for user in users]
    return users

def get_all_students_json():
    students = get_all_students()
    if not students:
        return []
    students = [student.to_json() for student in students]
    return students


def get_all_staff_json():
    staff_members = get_all_staff()
    if not staff_members:
        return []
    staff_members = [staff.to_json() for staff in staff_members]
    return staff_members

def get_all_users():
    return db.session.query(Admin).all() +  db.session.query(Staff).all() + db.session.query(Student).all()

def get_all_students():
    return db.session.query(Student).all()


def get_all_staff():
    return db.session.query(Staff).all()


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

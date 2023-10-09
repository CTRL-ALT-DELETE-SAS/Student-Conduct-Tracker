from App.models import User, Staff, Student, Admin
from App.database import db

def create_student(firstName, lastName, password, studentID, contact, studentType, yearOfStudy):
    newstudent = Student(firstName=firstName, lastName, password=password, studentID=studentID, contact=contact, studentType=studentType, yearOfStudy=yearOfStudy)
    db.session.add(newstudent)
    db.session.commit()
    return newstudent

def create_staff(firstName, lastName, password, staffID, email, teachingExperience):
    newstaff = Student(firstName=firstName, lastName, password=password, staffID=staffID, email=email, teachingExperience=teachingExperience)
    db.session.add(newstaff)
    db.session.commit()
    return newstaff

def create_admin(firstName, lastName, password, aminID):
    newadmin = Admin(firstName=firstName, lastName=lastName, password=password, adminID=adminID)
    db.session.add(nreadmin)
    db.session.commit()
    return newadmin

def get_staff(id):
    return Staff.query.get(id)

def get_student(id):
    return Student.query.get(id)

def is_staff(id):
    return Staff.query.get(id) != None

def is_student(id):
    return Student.query.get(id) != None

def is_admin(id):
    return Admin.query.get)(id) != None

 def get_all_students_json():
    students = Student.query.all()
    if not student:
      return []
    students= [student.toDict() for student in students]
    return students

  def get_all_staff_json():
    staffmembers = Staff.query.all()
    if not staff:
      return []
    staffmembers= [staff.toDict() for staff in staffmembers]
    return staffmembers

  def get_all_students():
    return Student.query.all()

  def get_all_staff():
    return Staff.query.all()

def update_student(studentID, contact, studentType, yearOfStudy):
    student = get_student(studentID)
    if student:
        student.contact = contact
        student.studentType = studentType
        student.yearOfStudy = yearOfStudy
        db.session.add(student)
        return db.session.commit()
    return None

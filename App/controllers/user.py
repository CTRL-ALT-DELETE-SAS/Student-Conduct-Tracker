from App.models import Staff, Student, Admin
from App.database import db


def create_student(admin, studentID, firstname, lastname, contact, studentType, yearofStudy):
    new_student = admin.addStudent(studentID, firstname=firstname, lastname=lastname, contact=contact, studentType=studentType, yearofStudy=yearofStudy)
	if new_student:
		return new_student
	return None


def create_staff(admin, staffID, firstname, lastname, password, email):
    new_staff = admin.addStaff(staffID, firstname=firstname, lastname=lastname, password=password, email=email)
    if new_staff:
        return new_staff
    return None


def create_admin(firstname, lastname, password):
    new_admin = Admin(firstname=firstname, lastname=lastname, password=password)
    db.session.add(new_admin)
    db.session.commit()
    return new_admin


def get_staff(staffID):
    return Staff.query.filter_by(id=staffID).first()


def get_student(studentID):
    return Student.query.filter_by(id=studentID).first()


def get_admin(adminID):
    return Admin.query.filter_by(id=adminID).first()


def is_staff(staffID):
    return db.session.query(Staff).get(staffID) is not None


def is_student(studentID):
    return db.session.query(Student).get(studentID) is not None


def is_admin(AdminID):
    return db.session.query(Admin).get(AdminID) is not None 


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


def update_student(student, firstname, lastname, contact, studentType, yearofStudy):
    student.firstname = firstname 
    student.lastname = lastname
    student.contact = contact
    student.studentType = studentType
    student.yearOfStudy = yearofStudy
    db.session.add(student)
    db.session.commit()
    return student
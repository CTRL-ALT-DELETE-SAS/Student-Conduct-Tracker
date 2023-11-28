from App.models import Admin
from App.database import db 

def add_student_information (admin, id, firstname, lastname, studentType, yearofEnrollment):
    return admin.addStudentInformation(id, firstname, lastname, studentType, yearofEnrollment)

def update_student (admin, studentID, field_to_update, new_value):
    return admin.updateStudent(studentID, field_to_update, new_value)
    
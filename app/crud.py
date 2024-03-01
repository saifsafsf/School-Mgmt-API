from sqlalchemy.orm import Session

from models import (
    Student,
    Subject,
    Teacher,
    Department,
    Enrollment
)
import schemas


def create_student(
        db: Session, 
        student: schemas.StudentCreate
    ):

    db_student = Student(**student.dict())
    db.add(db_student)
    
    db.commit()
    db.refresh(db_student)
    
    return db_student


def create_department(
        db: Session, 
        department: schemas.DepartmentCreate,
    ):

    db_dept = Department(**department.dict())
    db.add(db_dept)

    db.commit()
    db.refresh(db_dept)

    return db_dept


def create_subject(
        db: Session, 
        subject: schemas.SubjectCreate
    ):

    db_subject = Subject(
        **subject.dict()
    )
    db.add(db_subject)

    db.commit()
    db.refresh(db_subject)

    return db_subject


def create_teacher(
        db: Session, 
        teacher: schemas.TeacherCreate
    ):

    db_teacher = Teacher(**teacher.dict())
    db.add(db_teacher)

    db.commit()
    db.refresh(db_teacher)

    return db_teacher


def create_enrollment(
        db: Session, 
        enrollment: schemas.EnrollmentCreate
    ):

    db_enroll = Enrollment(**enrollment.dict())
    db.add(db_enroll)

    db.commit()
    db.refresh(db_enroll)

    return db_enroll


def get_student(db: Session, email: str):
    return (
        db
        .query(Student)
        .filter(Student.email == email)
        .first()
    )

def get_department(db: Session, dept_name: str):
    return (
        db
        .query(Department)
        .filter(Department.dept_name == dept_name)
        .first()
    )

def get_teacher(db: Session, email: str):
    return (
        db
        .query(Teacher)
        .filter(Teacher.email == email)
        .first()
    )

def get_subject(db: Session, subj_name: str):
    return (
        db
        .query(Subject)
        .filter(Subject.subj_name == subj_name)
        .first()
    )

def get_enrollment(db: Session, student_id: int, subject_id: int):
    return (
        db
        .query(Enrollment)
        .filter((Enrollment.student_id == student_id) & (Enrollment.subject_id == subject_id))
        .first()
    )

def get_subject_by_student(db: Session, student_id: int):

    enrollments = (
        db
        .query(Enrollment)
        .filter(Enrollment.student_id == student_id)
        .all()
    )

    subjects = []
    for enrollment in enrollments:
        subject = (
            db
            .query(Subject)
            .filter(Subject.id == enrollment.subject_id)
            .first()
        )

        if subject:
            subjects.append(subject)

    return subjects

def update_records(db: Session, update_request: schemas.UpdateRequest):
    try:
        for update_item in update_request.updates:
            table_name = update_item.table_name
            record_id = update_item.record_id
            updated_fields = update_item.updated_fields

            if table_name == "students":
                (
                    db
                    .query(Student)
                    .filter(Student.id == record_id)
                    .update(updated_fields)
                )

            elif table_name == "teachers":
                (
                    db
                    .query(Teacher)
                    .filter(Teacher.id == record_id)
                    .update(updated_fields)
                )

            elif table_name == "departments":
                (
                    db
                    .query(Department)
                    .filter(Department.id == record_id)
                    .update(updated_fields)
                )

            elif table_name == "subjects":
                (
                    db
                    .query(Subject)
                    .filter(Subject.id == record_id)
                    .update(updated_fields)
                )

            elif table_name == "students":
                (
                    db
                    .query(Student)
                    .filter(Student.id == record_id)
                    .update(updated_fields)
                )
            
            else:
                return False, f"Table '{table_name}' does not exist!"

        db.commit()
        return True, "Records updated successfully!"
    
    except Exception as e:
        db.rollback()
        return False, str(e)
    

def delete_enrollments(db: Session, student_id: int, subject_id: int):
    try:
        enrollment = (
            db
            .query(Enrollment)
            .filter((Enrollment.student_id == student_id) & (Enrollment.subject_id == subject_id))
            .first()
        )
        
        db.delete(enrollment)
        db.commit()
        return True, "Enrollment deleted successfully!"
    
    except Exception as e:
        db.rollback()
        return False, str(e)
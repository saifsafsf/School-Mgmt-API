from sqlalchemy.orm import Session
from typing import Optional, List

from models import (
    Student,
    Subject,
    Teacher,
    Department,
    Enrollment
)
from schemas import (
    StudentCreate,
    SubjectCreate,
    TeacherCreate,
    EnrollmentCreate,
    DepartmentCreate
)


def create_student(
        db: Session, 
        student: StudentCreate
    ):

    db_student = Student(**student.dict())
    db.add(db_student)
    
    db.commit()
    db.refresh(db_student)
    
    return db_student


def create_department(
        db: Session, 
        department: DepartmentCreate,
    ):

    db_dept = Department(**department.dict())
    db.add(db_dept)

    db.commit()
    db.refresh(db_dept)

    return db_dept


def create_subject(
        db: Session, 
        subject: SubjectCreate
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
        teacher: TeacherCreate
    ):

    db_teacher = Teacher(**teacher.dict())
    db.add(db_teacher)

    db.commit()
    db.refresh(db_teacher)

    return db_teacher


def create_enrollment(
        db: Session, 
        enrollment: EnrollmentCreate
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
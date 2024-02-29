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


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
    Subject,
    Teacher,
    Student,
    TeacherCreate,
    EnrollmentCreate,
    DepartmentCreate
)


def create_student(
        db: Session, 
        student: StudentCreate, 
        dept_id: int,
        subjects: Optional[List[Subject]] = None
    ):

    db_student = Student(**student.dict(), dept_id=dept_id)
    db.add(db_student)
    
    db.commit()
    db.refresh(db_student)

    if subjects:
        for subject in subjects:
            create_enrollment(
                db, 
                EnrollmentCreate(student_id=db_student.id, subject_id=subject.id)
            )
    
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
        subject: SubjectCreate,
        dept_id: int,
        teacher_id: int,
        students: Optional[List[Student]] = None
    ):

    db_subject = Subject(
        **subject.dict(), 
        dept_id=dept_id, 
        teacher_id=teacher_id
    )
    db.add(db_subject)

    db.commit()
    db.refresh(db_subject)
    
    if students:
        for student in students:
            create_enrollment(
                db, 
                EnrollmentCreate(student_id=student.id, subject_id=db_subject.id)
            )

    return db_subject


def create_teacher(
        db: Session, 
        teacher: TeacherCreate, 
        dept_id: int
    ):

    db_teacher = Teacher(**teacher.dict(), dept_id=dept_id)
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


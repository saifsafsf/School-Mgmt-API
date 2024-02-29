from pydantic import BaseModel
from typing import List, Optional


class DepartmentBase(BaseModel):
    name: str

class DepartmentCreate(DepartmentBase):
    pass

class Department(DepartmentBase):
    id : int

    class Config:
        orm_mode = True


class StudentBase(BaseModel):
    email: str
    name: str
    dept_id: int

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int

    class Config:
        orm_mode = True


class TeacherBase(BaseModel):
    email: str
    name: str
    dept_id: int

class TeacherCreate(TeacherBase):
    pass

class Teacher(TeacherBase):
    id: int

    class Config:
        orm_mode = True


class SubjectBase(BaseModel):
    name: str
    description: str
    dept_id: int

class SubjectCreate(SubjectBase):
    pass

class Subject(SubjectBase):
    id: int

    class Config:
        orm_mode = True


class EnrollmentBase(BaseModel):
    student_id: int
    subject_id: int

class EnrollmentCreate(EnrollmentBase):
    pass

class Enrollment(EnrollmentBase):
    pass

    class Config:
        orm_mode = True


class TeachingBase(BaseModel):
    teacher_id: int
    subject_id: int

class TeachingCreate(TeachingBase):
    pass

class Teaching(TeachingBase):
    pass

    class Config:
        orm_mode = True
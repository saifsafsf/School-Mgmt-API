from pydantic import BaseModel, validator
from typing import List, Dict, Any


class DepartmentBase(BaseModel):
    dept_name: str

class DepartmentCreate(DepartmentBase):
    pass

class Department(DepartmentBase):
    id : int

    class Config:
        orm_mode = True


class StudentBase(BaseModel):
    email: str
    std_name: str
    dept_id: int

    @validator('email')
    def email_must_be_valid_email(cls, value):
        
        if '@' not in value:
            raise ValueError('Invalid email format')
        
        return value


class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int

    class Config:
        orm_mode = True


class TeacherBase(BaseModel):
    email: str
    teacher_name: str
    dept_id: int

    @validator('email')
    def email_must_be_valid_email(cls, value):
        
        if '@' not in value:
            raise ValueError('Invalid email format')
        
        return value


class TeacherCreate(TeacherBase):
    pass

class Teacher(TeacherBase):
    id: int

    class Config:
        orm_mode = True


class SubjectBase(BaseModel):
    subj_name: str
    description: str
    dept_id: int
    teacher_id: int
    

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


class UpdateItem(BaseModel):
    table_name: str
    record_id: int
    updated_fields: Dict[str, Any]

class UpdateRequest(BaseModel):
    updates: List[UpdateItem]

class UpdateResponse(BaseModel):
    success: bool
    message: str
from sqlalchemy import (
    Column,
    Boolean,
    Integer,
    String,
    ForeignKey
)
from sqlalchemy.orm import relationship

from database import Base


class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    name = Column(String)
    email = Column(String, unique=True, index=True)
    dept_id = Column(Integer, ForeignKey('departments.id'))
    
    department = relationship('Department', back_populates='students')
    subjects = relationship('Enrollment', back_populates='students')


class Teacher(Base):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    name = Column(String)
    email = Column(String, unique=True, index=True)
    dept_id = Column(Integer, ForeignKey('departments.id'))
    
    subjects = relationship('Teaching', back_populates='teachers')
    department = relationship('Department', back_populates='teachers')


class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    name = Column(String, unique=True, index=True)

    students = relationship('Student', back_populates='department')
    teachers = relationship('Teacher', back_populates='department')


class Subject(Base):
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    name = Column(String, unique=True, index=True)
    description = Column(String)

    students = relationship('Enrollment', back_populates='subjects')
    teachers = relationship('Teaching', back_populates='subjects')


class Enrollment(Base):
    __tablename__ = 'enrollments'

    student_id = Column(Integer, ForeignKey('students.id'), primary_key=True)
    subject_id = Column(Integer, ForeignKey('subjects.id'), primary_key=True)

    students = relationship('Student', back_populates='subjects')
    subjects = relationship('Subject', back_populates='students')


class Teaching(Base):
    __tablename__ = 'teachings'

    teacher_id = Column(Integer, ForeignKey('teachers.id'), primary_key=True)
    subject_id = Column(Integer, ForeignKey('subjects.id'), primary_key=True)

    teachers = relationship('Teacher', back_populates='subjects')
    subjects = relationship('Subject', back_populates='teachers')
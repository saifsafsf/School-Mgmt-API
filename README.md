# Database Schema

## Overview

This database schema represents a simplified model for managing students, teachers, departments, subjects, and enrollments. It allows for tracking students' enrollment in subjects, teachers associated with subjects, and departments to which students and teachers belong.

## Schema

The schema consists of the following tables:

- `students`: Stores information about students.
- `teachers`: Stores information about teachers.
- `departments`: Stores information about departments.
- `subjects`: Stores information about subjects.
- `enrollments`: Represents the many-to-many relationship between students and subjects.

## DBML Representation

```dbml
Table students {
  id integer [primary key]
  std_name varchar
  email varchar [unique]
  dept_id integer
}

Table teachers {
  id integer [primary key]
  teacher_name varchar
  email varchar [unique]
  dept_id integer
}

Table departments {
  id integer [primary key]
  dept_name varchar [unique]
}

Table subjects {
  id integer [primary key]
  subj_name varchar [unique]
  dept_id integer
  teacher_id integer
  description varchar
}

Table enrollments {
  student_id integer [ref: > students.id, primary key]
  subject_id integer [ref: > subjects.id, primary key]
}

Ref: students.dept_id > departments.id
Ref: teachers.dept_id > departments.id
Ref: subjects.dept_id > departments.id
Ref: subjects.teacher_id > teachers.id

## ERD
https://dbdiagram.io/d/65e14cbacd45b569fb43136b
import models
import schemas
from database import SessionLocal, engine, Base


class SQLRepository:

    def __init__(self):

        Base.metadata.create_all(bind=engine)
        self.db = next(self.__get_db())


    def __get_db(self):
        """
        Provides a SQLAlchemy database session 
        to the caller within a context manager.
        """

        db = SessionLocal()

        try:
            yield db
        finally:
            db.close()

    
    def create_student(
            self,
            student: schemas.StudentCreate
        ):

        try:
            db_student = models.Student(**student.dict())
            self.db.add(db_student)
            
            self.db.commit()
            self.db.refresh(db_student)
            
            return True, "Student created successfully!"
        
        except Exception as e:
            self.db.rollback()
            return False, str(e)


    def create_department(
            self,
            department: schemas.DepartmentCreate,
        ):
            
        try:
            db_dept = models.Department(**department.dict())
            self.db.add(db_dept)

            self.db.commit()
            self.db.refresh(db_dept)

            return True, "Department created successfully!"
        
        except Exception as e:
            self.db.rollback()
            return False, str(e)


    def create_subject(
            self,
            subject: schemas.SubjectCreate
        ):

        try:
            db_subject = models.Subject(
                **subject.dict()
            )
            self.db.add(db_subject)

            self.db.commit()
            self.db.refresh(db_subject)
            
            return True, "Subject created successfully!"
        
        except Exception as e:
            self.db.rollback()
            return False, str(e)


    def create_teacher(
            self,
            teacher: schemas.TeacherCreate
        ):

        try:
            db_teacher = models.Teacher(**teacher.dict())
            self.db.add(db_teacher)

            self.db.commit()
            self.db.refresh(db_teacher)
            
            return True, "Teacher created successfully!"
        
        except Exception as e:
            self.db.rollback()
            return False, str(e)


    def create_enrollment(
            self,
            enrollment: schemas.EnrollmentCreate
        ):

        try:
            db_enroll = models.Enrollment(**enrollment.dict())
            self.db.add(db_enroll)

            self.db.commit()
            self.db.refresh(db_enroll)
            
            return True, "Enrollment created successfully!"
        
        except Exception as e:
            self.db.rollback()
            return False, str(e)


    def get_student_by_email(self, email: str):
        return (
            self.db
            .query(models.Student)
            .filter(models.Student.email == email)
            .first()
        )
    

    def get_student_by_id(self, id: str):
        return (
            self.db
            .query(models.Student)
            .filter(models.Student.id == id)
            .first()
        )


    def get_department(self, dept_name: str):
        return (
            self.db
            .query(models.Department)
            .filter(models.Department.dept_name == dept_name)
            .first()
        )


    def get_teacher(self, email: str):
        return (
            self.db
            .query(models.Teacher)
            .filter(models.Teacher.email == email)
            .first()
        )


    def get_subject(self, subj_name: str):
        return (
            self.db
            .query(models.Subject)
            .filter(models.Subject.subj_name == subj_name)
            .first()
        )


    def get_enrollment(self, student_id: int, subject_id: int):
        return (
            self.db
            .query(models.Enrollment)
            .filter(
                (models.Enrollment.student_id == student_id) 
                & (models.Enrollment.subject_id == subject_id)
            )
            .first()
        )


    def get_subject_by_student(self, student_id: int):

        enrollments = (
            self.db
            .query(models.Enrollment)
            .filter(models.Enrollment.student_id == student_id)
            .all()
        )

        subjects = []
        for enrollment in enrollments:
            subject = (
                self.db
                .query(models.Subject)
                .filter(models.Subject.id == enrollment.subject_id)
                .first()
            )

            if subject:
                subjects.append(subject)

        return subjects


    def update_records(self, update_request: schemas.UpdateRequest):
        try:
            for update_item in update_request.updates:
                table_name = update_item.table_name
                record_id = update_item.record_id
                updated_fields = update_item.updated_fields

                if table_name == "students":
                    (
                        self.db
                        .query(models.Student)
                        .filter(models.Student.id == record_id)
                        .update(updated_fields)
                    )

                elif table_name == "teachers":
                    (
                        self.db
                        .query(models.Teacher)
                        .filter(models.Teacher.id == record_id)
                        .update(updated_fields)
                    )

                elif table_name == "departments":
                    (
                        self.db
                        .query(models.Department)
                        .filter(models.Department.id == record_id)
                        .update(updated_fields)
                    )

                elif table_name == "subjects":
                    (
                        self.db
                        .query(models.Subject)
                        .filter(models.Subject.id == record_id)
                        .update(updated_fields)
                    )

                elif table_name == "students":
                    (
                        self.db
                        .query(models.Student)
                        .filter(models.Student.id == record_id)
                        .update(updated_fields)
                    )
                
                else:
                    return False, f"Table '{table_name}' does not exist!"

            self.db.commit()
            return True, "Records updated successfully!"
        
        except Exception as e:
            self.db.rollback()
            return False, str(e)
        

    def delete_enrollments(self, student_id: int, subject_id: int):
        try:
            enrollment = (
                self.db
                .query(models.Enrollment)
                .filter(
                    (models.Enrollment.student_id == student_id) 
                    & (models.Enrollment.subject_id == subject_id)
                )
                .first()
            )
            
            self.db.delete(enrollment)
            self.db.commit()
            return True, "Enrollment deleted successfully!"
        
        except Exception as e:
            self.db.rollback()
            return False, str(e)
        
    
    def delete_student(self, student_id: int):
        try:
            db_student = (
                self.db
                .query(models.Student)
                .filter(models.Student.id == student_id)
                .first()
            )

            self.db.delete(db_student)
            self.db.commit()
            return True, "Student deleted successfully!"
        
        except Exception as e:
            self.db.rollback()
            return False, str(e)
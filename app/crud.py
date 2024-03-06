import sys

sys.path.insert(0, "/home/")

from scripts import models, schemas
from scripts.database import SessionLocal, engine, Base


class SQLRepository:
    """
    A class to represent the data access layer. 
    """

    def __init__(self):
        """
        creates all the tables defined using declarative_base()
        
        Attributes
        ----------
        db : Session
            an instance of a database with all the tables defined in models.py
        """
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
        """
        creates the student record in the db

        Parameters
        ----------
        student : schemas.StudentCreate

        Returns
        -------
        success/failure, message : tuple
        """

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
        """
        creates the department record in the db

        Parameters
        ----------
        department : schemas.DepartmentCreate

        Returns
        -------
        success/failure, message : tuple
        """
            
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
        """
        creates the subject record in the db

        Parameters
        ----------
        subject : schemas.SubjectCreate

        Returns
        -------
        success/failure, message : tuple
        """

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
        """
        creates the teacher record in the db

        Parameters
        ----------
        teacher : schemas.TeacherCreate

        Returns
        -------
        success/failure, message : tuple
        """

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
        """
        creates the enrollment record in the db

        Parameters
        ----------
        enrollment : schemas.EnrollmentCreate

        Returns
        -------
        success/failure, message : tuple
        """

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
        """
        Fetches the student with the given email in the db

        Parameters
        ----------
        email : str
            the email of the student

        Returns
        -------
        models.Student
            the student record with matching email
        """

        return (
            self.db
            .query(models.Student)
            .filter(models.Student.email == email)
            .first()
        )
    

    def get_student_by_id(self, id: str):
        """
        Fetches the student with the given id in the db

        Parameters
        ----------
        id : int
            the id of the student

        Returns
        -------
        models.Student
            the student record with matching id
        """

        return (
            self.db
            .query(models.Student)
            .filter(models.Student.id == id)
            .first()
        )


    def get_department(self, dept_name: str):
        """
        Fetches the department with the given name in the db

        Parameters
        ----------
        dept_name : str
            the name of the department

        Returns
        -------
        models.Department
            the department record with matching name
        """

        return (
            self.db
            .query(models.Department)
            .filter(models.Department.dept_name == dept_name)
            .first()
        )


    def get_teacher(self, email: str):
        """
        Fetches the teacher with the given email in the db

        Parameters
        ----------
        email : str
            the email of the teacher

        Returns
        -------
        models.Teacher
            the teacher record with matching email
        """

        return (
            self.db
            .query(models.Teacher)
            .filter(models.Teacher.email == email)
            .first()
        )


    def get_subject(self, subj_name: str):
        """
        Fetches the subject with the given name in the db

        Parameters
        ----------
        subj_name : str
            the name of the subject

        Returns
        -------
        models.Subject
            the subject record with matching name
        """

        return (
            self.db
            .query(models.Subject)
            .filter(models.Subject.subj_name == subj_name)
            .first()
        )


    def get_enrollment(self, student_id: int, subject_id: int):
        """
        Fetches the enrollment with the given credentials

        Parameters
        ----------
        student_id : int
            the id of the student
        subject_id : int
            the id of the subject

        Returns
        -------
        models.Enrollment
            the enrollment with matching credentials
        """

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
        """
        Fetches the subject list for the given student

        Parameters
        ----------
        id : int
            the id of the student

        Returns
        -------
        list[models.Subject]
            the subject records with matching student in Enrollments table
        """

        enrollments = (
            self.db
            .query(models.Enrollment)
            .filter(models.Enrollment.student_id == student_id)
            .all()
        )

        subjects = []
        
        # for each subject the student is enrolled in
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
        """
        updates the the record with matching details

        Parameters
        ----------
        update_request : schemas.UpdateRequest
            List of schemas.UpdateItem to be updated

        Returns
        -------
        success/failure, message : tuple
        """
        
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
        """
        Deletes the enrollment with matching credentials

        Parameters
        ----------
        student_id : int
            the id of the student
        subject_id : int
            the id of the subject

        Returns
        -------
        success/failure, message : tuple
        """

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
        """
        Deletes the student with matching id

        Parameters
        ----------
        student_id : int
            the id of the student

        Returns
        -------
        success/failure, message : tuple
        """

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
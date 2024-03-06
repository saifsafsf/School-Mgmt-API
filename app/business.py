from fastapi import HTTPException
from io import StringIO
import json
import csv
import sys

sys.path.insert(0, "/home/")

from scripts import schemas
from crud import SQLRepository

# to have one repo throughout the whole system
REPO = SQLRepository()


class Uploader:
    """
    class to upload CSV or JSON payloads into the db
    """

    def __init__(self, repo=REPO):
        """
        Assigns the global SQL repo to the instance

        Parameters
        ----------
        repo : Optional[SQLRepository]
            The SQL Repository with all the functions related to the db
        """
        self.repo = repo

    
    def upload_csv(self, file_content: bytes):
        """
        Takes the file content of the CSV payload
        and inserts into the db

        Parameters
        ----------
        file_content : bytes
            binary content of the file

        Returns
        -------
        success/failure, message : tuple

        Raises
        ------
        HTTPException
            If the insertion is not successful
        """

        content_str = file_content.decode('utf-8')
        data = csv.DictReader(StringIO(content_str))

        for row in data:
            for col in row:

                if 'dept_name' == col:
                    # finding if the dept already exists
                    db_dept = self.repo.get_department(
                        dept_name=row.get('dept_name')
                    )

                    # in CSV bulk insertions, ignore if it exists
                    if db_dept:
                        continue
                    
                    try:
                        success, message = self.repo.create_department(
                            department=schemas.DepartmentCreate(dept_name=row.get('dept_name'))
                        )
                    except Exception as e:
                        success, message = False, str(e)

                elif 'teacher_name' == col:
                    db_teacher = self.repo.get_teacher(
                        email=row.get('teacher_email')
                    )

                    if db_teacher:
                        continue
                    
                    try:
                        success, message = self.repo.create_teacher(
                            teacher=schemas.TeacherCreate(
                                email=row.get('teacher_email'),
                                teacher_name=row.get('teacher_name'),
                                dept_id=row.get('dept_id')
                            )
                        )
                    except Exception as e:
                        success, message = False, str(e)

                elif 'subj_name' == col:
                    db_subj = self.repo.get_subject(
                        subj_name=row.get('subj_name')
                    )

                    if db_subj:
                        continue

                    try:
                        success, message = self.repo.create_subject(
                            subject=schemas.SubjectCreate(
                                subj_name=row.get('subj_name'),
                                description=row.get('description'),
                                dept_id=row.get('dept_id'),
                                teacher_id=row.get('teacher_id')
                            )
                        )
                    except Exception as e:
                        success, message = False, str(e)
                
                elif 'std_name' == col:
                    db_stud = self.repo.get_student_by_id(
                        id=row.get('std_id')
                    )

                    if db_stud:
                        continue

                    try:
                        success, message = self.repo.create_student(
                            student=schemas.StudentCreate(
                                email=row.get('std_email'),
                                std_name=row.get('std_name'),
                                dept_id=row.get('dept_id')
                            )
                        )
                    except Exception as e:
                        success, message = False, str(e)

                else:
                    success = True
                    continue

                if not success:
                    raise HTTPException(status_code=400, detail=message)
                
            if ('subj_name' in row) and ('std_name' in row):
                db_enroll = self.repo.get_enrollment(
                    student_id=row.get('std_id'),
                    subject_id=row.get('subj_id')
                )

                if db_enroll:
                    continue
                
                try:
                    success, message = self.repo.create_enrollment(
                        enrollment=schemas.EnrollmentCreate(
                            student_id=row.get('std_id'),
                            subject_id=row.get('subj_id')
                        )
                    )
                except Exception as e:
                    success, message = False, str(e)

                if not success:
                    raise HTTPException(status_code=400, detail=message)

        return {
            "success": success, 
            "message": "Data Inserted Successfully!"
        }
    

    def upload_json(self, file_content: bytes):
        """
        Takes the file content of the JSON payload
        and inserts into the db

        Parameters
        ----------
        file_content : bytes
            binary content of the file

        Returns
        -------
        success/failure, message : tuple

        Raises
        ------
        HTTPException
            If the insertion is not successful
            OR If a record already exists in the db
        """

        content_str = file_content.decode('utf-8')
        data = json.loads(content_str)

        for row in data:
            if 'dept_name' in row:
                # if the dept already exists
                db_dept = self.repo.get_department(
                    dept_name=row.get('dept_name')
                )

                # raise an exception, halt the process
                if db_dept:
                    raise HTTPException(status_code=400, detail="Department already exists.")
                
                try:
                    success, message = self.repo.create_department(
                        department=schemas.DepartmentCreate(**row)
                    )
                except Exception as e:
                    success, message = False, str(e)

            elif 'std_name' in row:
                db_stud = self.repo.get_student_by_email(
                    email=row.get('email')
                )

                if db_stud:
                    raise HTTPException(status_code=400, detail="Student already exists!")

                try:
                    success, message = self.repo.create_student(
                        student=schemas.StudentCreate(**row)
                    )
                except Exception as e:
                    success, message = False, str(e)
            
            elif 'subj_name' in row:
                db_subj = self.repo.get_subject(
                    subj_name=row.get('subj_name')
                )

                if db_subj:
                    raise HTTPException(status_code=400, detail="Subject already exists!")

                try:
                    success, message = self.repo.create_subject(
                        subject=schemas.SubjectCreate(**row)
                    )
                except Exception as e:
                    success, message = False, str(e)
            
            elif 'teacher_name' in row:
                db_teacher = self.repo.get_teacher(
                    email=row.get('email')
                )

                if db_teacher:
                    raise HTTPException(status_code=400, detail="Teacher already exists!")
                
                try:
                    success, message = self.repo.create_teacher(
                        teacher=schemas.TeacherCreate(**row)
                    )
                except Exception as e:
                    success, message = False, str(e)
            
            elif ('subject_id' in row) and ('student_id'  in row):
                db_enroll = self.repo.get_enrollment(
                    student_id=row.get('student_id'),
                    subject_id=row.get('subject_id')
                )

                if db_enroll:
                    raise HTTPException(status_code=400, detail="Enrollment already exists!")
                
                try:
                    success, message = self.repo.create_enrollment(
                        enrollment=schemas.EnrollmentCreate(**row)
                    )
                except Exception as e:
                    success, message = False, str(e)

            else:
                pass

            if not success:
                raise HTTPException(status_code=400, detail=message)

        return {
            "success": success, 
            "message": "Data Inserted Successfully!"
        }
    

class Getter:
    """
    a class to get any record from the db
    """

    def __init__(self, repo=REPO):
        """
        Assigns the global SQL repo to the instance

        Parameters
        ----------
        repo : Optional[SQLRepository]
            The SQL Repository with all the functions related to the db
        """

        self.repo = repo

    
    def get_subjects_by_student(self, student_id):
        """
        Fetches the subject list for the given student

        Parameters
        ----------
        student_id : int
            the id of the student

        Returns
        -------
        list[models.Subject]
            the subject records with matching student in Enrollments table
        """

        db_student = self.repo.get_student_by_id(id=student_id)

        if not db_student:
            raise HTTPException(status_code=400, detail="Student does not exist!")

        subjects = self.repo.get_subject_by_student(
            student_id=student_id
        )

        return subjects
    

class Setter:
    """
    a class to update one or more records in the db
    """

    def __init__(self, repo=REPO):
        """
        Assigns the global SQL repo to the instance

        Parameters
        ----------
        repo : Optional[SQLRepository]
            The SQL Repository with all the functions related to the db
        """

        self.repo = repo

    
    def update_record(self, file_content: bytes):
        """
        Takes the file content of JSON payload 
        and updates the records with matching details

        Parameters
        ----------
        file_content : bytes
            binary content of the file

        Returns
        -------
        success/failure, message : tuple

        Raises
        ------
        HTTPException
            If the updating is not successful
        """

        content_str = file_content.decode('utf-8')
        data = json.loads(content_str)

        update_request = []
        for row in data:
            update_request.append(schemas.UpdateItem(**row))

        success, message = self.repo.update_records(
            update_request=schemas.UpdateRequest(updates=update_request)
        )

        if not success:
            raise HTTPException(status_code=400, detail=message)
        
        return {"success": success, "message": message}
    

class Deleter:
    """
    class to delete a record from the db
    """

    def __init__(self, repo=REPO):
        """
        Assigns the global SQL repo to the instance

        Parameters
        ----------
        repo : Optional[SQLRepository]
            The SQL Repository with all the functions related to the db
        """

        self.repo = repo

    
    def delete_enrollment(self, student_id: int, subject_id: int):
        """
        Takes the file content of JSON payload 
        and updates the records with matching details

        Parameters
        ----------
        file_content : bytes
            binary content of the file

        Returns
        -------
        success/failure, message : tuple

        Raises
        ------
        HTTPException
            If the updating is not successful
        """
        
        db_enroll = self.repo.get_enrollment(
            student_id=student_id,
            subject_id=subject_id
        )

        if not db_enroll:
            raise HTTPException(status_code=400, detail="Enrollment not found!")

        success, message = self.repo.delete_enrollments(
            student_id=student_id,
            subject_id=subject_id
        )

        if not success: 
            raise HTTPException(status_code=400, detail=message)
        return {"success": True, "message": message}

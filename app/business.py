from fastapi import HTTPException
from io import StringIO
import schemas
import json
import csv

from crud import SQLRepository


class Uploader:

    def __init__(self, repo=SQLRepository()):
        self.repo = repo

    
    def upload_csv(self, file_content: bytes):
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
                    
                    success, message = self.repo.create_department(
                        department=schemas.DepartmentCreate(dept_name=row.get('dept_name'))
                    )

                elif 'teacher_name' == col:
                    db_teacher = self.repo.get_teacher(
                        email=row.get('teacher_email')
                    )

                    if db_teacher:
                        continue
                    
                    success, message = self.repo.create_teacher(
                        teacher=schemas.TeacherCreate(
                            email=row.get('teacher_email'),
                            teacher_name=row.get('teacher_name'),
                            dept_id=row.get('dept_id')
                        )
                    )

                elif 'subj_name' == col:
                    db_subj = self.repo.get_subject(
                        subj_name=row.get('subj_name')
                    )

                    if db_subj:
                        continue

                    success, message = self.repo.create_subject(
                        subject=schemas.SubjectCreate(
                            subj_name=row.get('subj_name'),
                            description=row.get('description'),
                            dept_id=row.get('dept_id'),
                            teacher_id=row.get('teacher_id')
                        )
                    )
                
                elif 'std_name' == col:
                    db_stud = self.repo.get_student(
                        email=row.get('std_email')
                    )

                    if db_stud:
                        continue

                    success, message = self.repo.create_student(
                        student=schemas.StudentCreate(
                            email=row.get('std_email'),
                            std_name=row.get('std_name'),
                            dept_id=row.get('dept_id')
                        )
                    )

                else:
                    pass

                if not success:
                    raise HTTPException(status_code=400, details=message)
                
            if ('subj_name' in row) and ('std_name' in row):
                db_enroll = self.repo.get_enrollment(
                    student_id=row.get('std_id'),
                    subject_id=row.get('subj_id')
                )

                if db_enroll:
                    continue
                
                success, message = self.repo.create_enrollment(
                    enrollment=schemas.EnrollmentCreate(
                        student_id=row.get('std_id'),
                        subject_id=row.get('subj_id')
                    )
                )

                if not success:
                    raise HTTPException(status_code=400, details=message)

        return {
            "success": success, 
            "message": "Data Inserted Successfully!"
        }
    

    def upload_json(self, file_content: bytes):
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
                    raise HTTPException(status_code=400, details="Department already exists.")
                
                success, message = self.repo.create_department(
                    department=schemas.DepartmentCreate(**row)
                )

            elif 'std_name' in row:
                db_stud = self.repo.get_student_by_email(
                    email=row.get('email')
                )

                if db_stud:
                    raise HTTPException(status_code=400, details="Student already exists!")

                success, message = self.repo.create_student(
                    student=schemas.StudentCreate(**row)
                )
            
            elif 'subj_name' in row:
                db_subj = self.repo.get_subject(
                    subj_name=row.get('subj_name')
                )

                if db_subj:
                    raise HTTPException(status_code=400, details="Subject already exists!")

                success, message = self.repo.create_subject(
                    subject=schemas.SubjectCreate(**row)
                )
            
            elif 'teacher_name' in row:
                db_teacher = self.repo.get_teacher(
                    email=row.get('email')
                )

                if db_teacher:
                    raise HTTPException(status_code=400, details="Teacher already exists!")
                
                success, message = self.repo.create_teacher(
                    teacher=schemas.TeacherCreate(**row)
                )
            
            elif ('subject_id' in row) and ('student_id'  in row):
                db_enroll = self.repo.get_enrollment(
                    student_id=row.get('student_id'),
                    subject_id=row.get('subject_id')
                )

                if db_enroll:
                    raise HTTPException(status_code=400, details="Enrollment already exists!")
                
                success, message = self.repo.create_enrollment(
                    enrollment=schemas.EnrollmentCreate(**row)
                )

            else:
                pass

            if not success:
                raise HTTPException(status_code=400, details=message)

        return {
            "success": success, 
            "message": "Data Inserted Successfully!"
        }
    

class Getter:

    def __init__(self, repo=SQLRepository()):
        self.repo = repo

    
    def get_subjects_by_student(self, student_id):

        db_student = self.repo.get_student_by_id(id=student_id)

        if not db_student:
            raise HTTPException(status_code=400, details="Student does not exist!")

        subjects = self.repo.get_subject_by_student(
            student_id=student_id
        )

        return subjects
    

class Setter:

    def __init__(self, repo=SQLRepository()):
        self.repo = repo

    
    def update_record(self, file_content: bytes):
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

    def __init__(self, repo=SQLRepository()):
        self.repo = repo

    
    def delete_enrollment(self, student_id: int, subject_id: int):
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

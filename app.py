import uvicorn
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import json

from database import SessionLocal, engine, Base
import crud
import schemas
import models

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.post('/upload/')
async def upload_data(
        file: UploadFile = File(...),
        db: Session = Depends(get_db)
    ):
    
    content = await file.read()
    content_str = content.decode('utf-8')
    data = json.loads(content_str)

    for row in data:

        if 'dept_name' in row:
            db_dept = crud.get_department(
                db=db, 
                dept_name=row.get('dept_name')
            )

            if db_dept:
                raise HTTPException(status_code=400, detail="Department already exists!")
            
            crud.create_department(
                db=db, 
                department=schemas.DepartmentCreate(**row)
            )

        elif 'std_name' in row:
            db_stud = crud.get_student(
                db=db,
                email=row.get('email')
            )

            if db_stud:
                raise HTTPException(status_code=400, detail="Student already exists!")

            crud.create_student(
                db=db,
                student=schemas.StudentCreate(**row)
            )
        
        elif 'subj_name' in row:
            db_subj = crud.get_subject(
                db=db,
                subj_name=row.get('subj_name')
            )

            if db_subj:
                raise HTTPException(status_code=400, detail="Subject already exists!")

            crud.create_subject(
                db=db,
                subject=schemas.SubjectCreate(**row)
            )
        
        elif 'teacher_name' in row:
            db_teacher = crud.get_teacher(
                db=db,
                email=row.get('email')
            )

            if db_teacher:
                raise HTTPException(status_code=400, detail="Teacher already exists!")
            
            crud.create_teacher(
                db=db,
                teacher=schemas.TeacherCreate(**row)
            )
        
        elif ('subject_id' in row) and ('student_id'  in row):
            db_enroll = crud.get_enrollment(
                db=db,
                student_id=row.get('student_id'),
                subject_id=row.get('subject_id')
            )

            if db_enroll:
                raise HTTPException(status_code=400, detail="Enrollment already exists!")
            
            crud.create_enrollment(
                db=db,
                enrollment=schemas.EnrollmentCreate(**row)
            )

        else:
            pass

    return {"message": "Data Inserted Successfully!"}


@app.get('/students/{student_id}/subjects/')
def get_subjects_by_student(
        student_id: int, 
        db: Session = Depends(get_db)
    ):

    db_student = (
        db
        .query(models.Student)
        .filter(models.Student.id == student_id)
        .first()
    )

    if not db_student:
        raise HTTPException(status_code=404, detail="Student does not exists!")

    subjects = crud.get_subject_by_student(
        db=db,
        student_id=student_id
    )

    return subjects

@app.put('/update/')
async def update_record(
        file: UploadFile = File(...), 
        db: Session = Depends(get_db)
    ):

    try:
        content = await file.read()
        content_str = content.decode('utf-8')
        data = json.loads(content_str)

        update_request = []
        for row in data:
            update_request.append(schemas.UpdateItem(**row))

        success, message = crud.update_records(
            db=db,
            update_request=schemas.UpdateRequest(updates=update_request)
        )

        if not success:
            raise HTTPException(status_code=400, detail=message)
        
        return {"success": True, "message": message}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get('/')
def home_page():
    return {"message": "This is HOME!"}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=5000)
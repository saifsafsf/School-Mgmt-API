import uvicorn
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import json

from database import SessionLocal, engine, Base
from crud import (
    create_department,
    create_enrollment,
    create_student,
    create_subject,
    create_teacher,
)
from schemas import (
    StudentCreate,
    SubjectCreate,
    TeacherCreate,
    DepartmentCreate,
    EnrollmentCreate
)

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.post('/upload/dept/')
async def upload_departments(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    
    content = await file.read()
    contents = content.decode('utf-8')
    data = json.loads(contents)

    for row in data:

        if 'dept_name' in row:
            create_department(
                db=db, 
                department=DepartmentCreate(**row)
            )

        elif 'std_name' in row:
            create_student(
                db=db,
                student=StudentCreate(**row)
            )
        
        elif 'subj_name' in row:
            create_subject(
                db=db,
                subject=SubjectCreate(**row)
            )
        
        elif 'teacher_name' in row:
            create_teacher(
                db=db,
                teacher=TeacherCreate(**row)
            )
        
        elif ('subject_id' in row) and ('student_id'  in row):
            create_enrollment(
                db=db,
                enrollment=EnrollmentCreate(**row)
            )

        else:
            pass

    return {"message": "Data Inserted Successfully!"}

@app.get('/')
def home_page():
    return {"message": "This is HOME!"}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=5000)
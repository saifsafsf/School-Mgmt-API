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


# Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@app.post('/upload')
async def upload_departments(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    
    content = await file.read()
    contents = content.decode('utf-8')
    data = json.loads(contents)

    for row in data:
        create_department(
            db=db, 
            department=DepartmentCreate(**row)
        )


@app.get('/')
def home_page():
    return {"message": "This is HOME!"}

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=5000)
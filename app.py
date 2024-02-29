import uvicorn
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import json

from database import SessionLocal, engine
from models import (
    Teacher,
    Teaching,
    Department,
    Student,
    Subject,
    Enrollment
)


app = FastAPI()

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@app.post('/upload')
async def upload_payload(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    
    content = await file.read()
    contents = content.decode('utf-8')
    data = json.loads(contents)

    for item in data:
        pass


@app.get('/')
def home_page():
    return {"message": "This is HOME!"}

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=5000)
import uvicorn
from fastapi import FastAPI, UploadFile, File
from typing import Literal
import sys

sys.path.insert(0, "C:\\NUST\\Jobs\\Sila")

from app import (
    GETTER,
    SETTER,
    UPLOADER,
    DELETER
)


app = FastAPI()


@app.post('/upload')
async def upload_data(
        format: Literal['csv', 'json'],
        file: UploadFile = File(...)
    ):
    """
    Endpoint to upload CSV data and insert it into the database.

    Parameters
    ----------
    file : UploadFile
        the CSV file to be uploaded
    """

    # waiting for the uploading file
    content = await file.read()

    if format == 'csv':
        message = UPLOADER.upload_csv(content)
    elif format == 'json':
        message = UPLOADER.upload_json(content)
    else:
        raise ValueError('Invalid Value for `format` parameter. Expected `csv` or `json`.')

    return message


@app.get('/students/{student_id}/subjects')
def get_subjects_by_student(student_id: int):
    """
    Retrieve subjects enrolled by a specific student.

    Parameters
    ----------
    student_id : int
        the student's id in the db
    """

    subjects = GETTER.get_subjects_by_student(student_id)

    return subjects


@app.put('/update')
async def update_record(
        file: UploadFile = File(...)
    ):
    """
    Updates the given fields of the records.

    Parameters
    ----------
    file : UploadFile
        the JSON file to be uploaded
    """

    content = await file.read()
    message = SETTER.update_record(content)

    return message   


@app.delete('/delete')
def delete_enrollment(student_id: int, subject_id: int):
    """
    Deletes the enrollment of a student

    Parameters
    ----------
    student_id : int
        the student's id in the db
    subject_id : int
        the subject's id in the db
    """

    message = DELETER.delete_enrollment(
        student_id=student_id, 
        subject_id=subject_id
    )

    return message


@app.get('/')
def home_page():
    return {"message": "This is HOME!"}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=5000)
import uvicorn
from fastapi import FastAPI, UploadFile, File
from typing import Literal

from business import (
    Uploader,
    Getter,
    Setter,
    Deleter
)

app = FastAPI()
uploader = Uploader()
getter = Getter()
setter = Setter()
deleter = Deleter()


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
        message = uploader.upload_csv(content)
    elif format == 'json':
        message = uploader.upload_json(content)
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

    subjects = getter.get_subjects_by_student(student_id)

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
    message = setter.update_record(content)

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

    message = deleter.delete_enrollment(
        student_id=student_id, 
        subject_id=subject_id
    )

    return message


@app.get('/')
def home_page():
    return {"message": "This is HOME!"}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=5000)
import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def home_page():
    return {"message": "This is HOME!"}

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=5000)
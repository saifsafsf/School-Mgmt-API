FROM python:3.11.3

WORKDIR /home

COPY requirements.txt .

RUN pip install -r requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/"

COPY ./ /home/
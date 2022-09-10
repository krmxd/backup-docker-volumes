FROM python:3.10.7-alpine

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY *.py .

CMD ["python3", "/app/run.py"]
FROM python:3.11

WORKDIR /app

ENV WATCHED_FOLDER="/app/to-watch"
ENV PATIENT_ID=
ENV KAFKA_BOOTSTRAP_SERVERS=

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["python", "main.py"]
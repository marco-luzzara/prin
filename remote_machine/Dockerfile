FROM python:3.11

WORKDIR /app

ENV FLASK_KAFKA_BOOTSTRAP_SERVERS=

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 80

ENTRYPOINT ["flask", "--app", "webapp", "run", "--port", "80", "--host", "0.0.0.0"]
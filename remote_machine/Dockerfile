FROM python:3.10

WORKDIR /app

VOLUME /app/to-watch

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["python", "main.py", "/app/to-watch"]
FROM python:3.12

WORKDIR /app

ENV KAFKA_BOOTSTRAP_SERVERS=
ENV OWNER_ID=

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=10s --start-period=1m --retries=3 CMD ["curl", "http://localhost/health"]

ENTRYPOINT ["flask", "--app", "webapp", "run", "--port", "80", "--host", "0.0.0.0"]
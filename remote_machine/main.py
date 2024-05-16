import time
import os
import logging
import socket
import dataclasses
from typing import Callable, List
from .PatientRecord import PatientRecord

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler, FileSystemEvent

import pandas as pd
import json

from confluent_kafka import Producer

def get_env_or_throw_if_empty(env: str) -> str:
    env_value = os.getenv(env)
    if env_value is not None and len(env_value) > 0:
        return env_value
    else:
        raise Exception(f'environment variable {env} must be non-empty')

WATCHED_FOLDER = get_env_or_throw_if_empty('WATCHED_FOLDER')
KAFKA_BOOTSTRAP_SERVERS = get_env_or_throw_if_empty('KAFKA_BOOTSTRAP_SERVERS')

def cast_excel_to_objs_list(excel_path: str) -> List[PatientRecord]:
    df = pd.read_excel(excel_path)
    return [PatientRecord.from_dict(obj) for obj in json.loads(df.to_json(orient='records'))]


class PatientRecordConsumer:
    def __init__(self, producer: Producer):
        self.producer = producer

    def consume(self, patient_record: PatientRecord) -> None:
        patient_dict = dataclasses.asdict(patient_record)
        del patient_dict['patient_id']
        self.producer.produce('filesystemwatcher.medical-records', 
                              key=patient_record.patient_id, 
                              value=json.dumps(patient_dict).encode())


class XslFileEventHandler(PatternMatchingEventHandler):
    def __init__(self, record_consumer: Callable[[PatientRecord], None]):
        # include only the excel files, the events for other file types are ignored
        super().__init__(['*.xls', '*.xlsx', '*.ods'], ignore_directories=True)
        self.record_consumer = record_consumer

    def on_created(self, event: FileSystemEvent) -> None:
        logging.info(f'Excel file found: {event.src_path}...')
        patient_records = cast_excel_to_objs_list(event.src_path)

        for patient_record in patient_records:
            logging.info(f'|___Patient found: {patient_record}')
            self.record_consumer(patient_record)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # bootstrap.servers does not require the complete list of nodes
    # https://stackoverflow.com/q/61656223/5587393
    kafka_conf = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'client.id': socket.gethostname()
    }
    kafka_producer = Producer(kafka_conf)

    logging.info(f'Start watching directory {WATCHED_FOLDER!r}')

    kafka_pub = PatientRecordConsumer(kafka_producer)
    event_handler = XslFileEventHandler(kafka_pub.consume)
    
    observer = Observer()
    observer.schedule(event_handler, WATCHED_FOLDER, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()
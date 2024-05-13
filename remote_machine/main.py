import sys
import time
import os
import logging
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler, FileSystemEvent

import pandas as pd

from confluent_kafka import Producer
import socket

def get_env_or_throw_if_empty(env: str) -> str:
    env_value = os.getenv(env)
    if env_value is not None and len(env_value) > 0:
        return env_value
    else:
        raise f'environment variable {env} must be non-empty'

WATCHED_FOLDER = get_env_or_throw_if_empty('WATCHED_FOLDER')
PATIENT_ID = get_env_or_throw_if_empty('PATIENT_ID')
KAFKA_BOOTSTRAP_SERVERS = get_env_or_throw_if_empty('KAFKA_BOOTSTRAP_SERVERS')

class EventProcessor:
    def __init__(self, event: FileSystemEvent):
        self.path = event.src_path

    def process(self) -> bytes:
        df = pd.read_excel(self.path)
        csv_file = df.to_csv()
        csv_file_bytes = csv_file.encode('utf-8')

        return csv_file_bytes
    
class FileProcessor:
    def process(self, file: bytes) -> None:
        raise 'subclass me'

class KafkaFileProcessor(FileProcessor):
    def __init__(self, producer: Producer):
        self.producer = producer

    def process(self, file: bytes) -> None:
        self.producer.produce('filesystemwatcher.medical-records', key=PATIENT_ID, value=file)


class XslFileEventHandler(PatternMatchingEventHandler):
    def __init__(self, fileProcessor: FileProcessor):
        #include only the excel files, the events for other file types are ignored
        super().__init__(['*.xls', '*.xlsx', '*.ods'], ignore_directories=True)
        self.fileProcessor = fileProcessor

    def on_created(self, event: FileSystemEvent) -> None:
        eventProcessor = EventProcessor(event)
        csv_file_bytes = eventProcessor.process()

        # show only the first 10 byte of a CSV
        csv_overview = str(csv_file_bytes[0:10]) + ('...' if len(csv_file_bytes) > 10 else '')
        logging.info(f'Excel file found: {event.src_path}: {csv_overview}')

        self.fileProcessor.process(csv_file_bytes)

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

    fileProcessor = KafkaFileProcessor(kafka_producer)
    event_handler = XslFileEventHandler(fileProcessor)
    
    observer = Observer()
    observer.schedule(event_handler, WATCHED_FOLDER, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()
import dataclasses
import json
import socket
from typing import Dict
from confluent_kafka import Producer

from .model.PatientRecord import PatientRecord

from abc import ABC, abstractmethod

class RecordProcessor(ABC):
    @abstractmethod
    def __init__(self, configs: Dict[str, str]):
        pass

    @abstractmethod
    def consume(self, patient_record: PatientRecord) -> None:
        pass

class KafkaProcessor(RecordProcessor):
    def __init__(self, configs: Dict[str, str]):
        kafka_conf = {
            'bootstrap.servers': configs['KAFKA_BOOTSTRAP_SERVERS'],
            'client.id': socket.gethostname()
        }
        self.producer = Producer(kafka_conf)

    def consume(self, patient_record: PatientRecord) -> None:
        patient_dict = dataclasses.asdict(patient_record)
        del patient_dict['id']
        self.producer.produce('filesystemwatcher.medical-records', 
                              key=patient_record.id.to_bytes(8, 'big'), 
                              value=json.dumps(patient_dict).encode())
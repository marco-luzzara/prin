import dataclasses
import json
import socket
from typing import Dict, Any
from confluent_kafka import Producer

from abc import ABC, abstractmethod

class RecordProcessor(ABC):
    @abstractmethod
    def __init__(self, configs: Dict[str, str]):
        pass

    @abstractmethod
    def consume(self, destionation, id, data) -> None:
        pass

class KafkaProcessor(RecordProcessor):
    def __init__(self, configs: Dict[str, str]):
        kafka_conf = {
            'bootstrap.servers': configs['KAFKA_BOOTSTRAP_SERVERS'],
            'client.id': socket.gethostname()
        }
        self.producer = Producer(kafka_conf)

    def consume(self, destination, id, data: Dict[str, Any]) -> None:
        self.producer.produce(destination, 
                              key=json.dumps({ 'id': id }).encode(), 
                              value=json.dumps(data).encode())
import os
import json
import socket

import flask
from kafka import KafkaProducer, KafkaConsumer
import logging

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', '')
if KAFKA_BOOTSTRAP_SERVERS == '':
    raise Exception('Env variable KAFKA_BOOTSTRAP_SERVERS is empty')

_kafka_producer = None
_kafka_consumer = None

def create_app(test_config=None):
    app = flask.Flask(__name__, instance_relative_config=True)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Loading configurations...')
    if test_config is None:
        app.config.from_mapping({})
    else:
        app.config.from_mapping(test_config)

    app.logger.info('Configurations loaded')

    os.makedirs(app.instance_path)

    app.logger.info('Initializing Kafka Clients...')
    configure_kafka_clients()
    app.logger.info('Kafka Clients initialized')

    from .routes import patients_data_loading, mir_results_data_loading, task_runner, users
    app.register_blueprint(patients_data_loading.bp)
    app.register_blueprint(mir_results_data_loading.bp)
    app.register_blueprint(task_runner.bp)
    app.register_blueprint(users.bp)

    @app.get('/health')
    def health_check():
        return ('', 200)

    return app


def configure_kafka_clients():
    global _kafka_producer, _kafka_consumer
    _kafka_producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        client_id=f'edge-vm-{socket.gethostname()}',
        value_serializer=lambda m: json.dumps(m).encode(),
        key_serializer=lambda m: json.dumps(m).encode()
    )

    _kafka_consumer = KafkaConsumer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        client_id=f'edge-vm-{socket.gethostname()}',
        value_deserializer=lambda m: json.loads(m.decode())
    )

import dataclasses
import os
import socket

from confluent_kafka import Producer
import flask
import logging
from . import record_processors

record_processor: record_processors.RecordProcessor = None

def create_app(test_config=None):
    app = flask.Flask(__name__, instance_relative_config=True)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Loading configurations...')
    if test_config is None:
        app.config.from_prefixed_env()
        app.config['RECORD_PROCESSOR_CLASS'] = 'KafkaProcessor'
    else:
        app.config.from_mapping(test_config)
    app.logger.info('Configurations loaded')

    try:
        os.makedirs(app.instance_path)
    except OSError as exc:
        app.logger.warning(exc)
        pass

    app.logger.info('Initializing RecordProcessor...')
    global record_processor
    record_processor = configure_record_processor(app)
    app.logger.info('RecordProcessor initialized')

    from . import data_loading
    app.register_blueprint(data_loading.bp)

    return app


def configure_record_processor(app: flask.Flask):
    RecordProcessorClass: record_processors.RecordProcessor = \
        getattr(record_processors, app.config['RECORD_PROCESSOR_CLASS'])
    app.logger.info(f'RecordProcessor set to {RecordProcessorClass.__name__}')

    return RecordProcessorClass(dict(app.config))
import os
from typing import Dict, Any

import flask
import logging
from . import record_processors

record_processor: record_processors.RecordProcessor = None

def create_app(test_config=None):
    app = flask.Flask(__name__, instance_relative_config=True)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Loading configurations...')
    if test_config is None:
        app.config['RECORD_PROCESSOR_CLASS'] = os.environ.get('RECORD_PROCESSOR_CLASS', 'KafkaProcessor')
        app.config['KAFKA_BOOTSTRAP_SERVERS'] = os.environ['KAFKA_BOOTSTRAP_SERVERS']
        app.config['OWNER_ID'] = os.environ['OWNER_ID']
    else:
        app.config.from_mapping(test_config)
        # configs = ...
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

    from .routes import patients_data_loading, pcr_results_data_loading
    app.register_blueprint(patients_data_loading.bp)
    app.register_blueprint(pcr_results_data_loading.bp)

    @app.get('/health')
    def health_check():
        return ('', 200)

    return app


def configure_record_processor(app: flask.Flask) -> record_processors.RecordProcessor:
    RecordProcessorClass: record_processors.RecordProcessor = \
        getattr(record_processors, app.config['RECORD_PROCESSOR_CLASS'])
    app.logger.info(f'RecordProcessor set to {RecordProcessorClass.__name__}')

    return RecordProcessorClass(app)
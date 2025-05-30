import os
from typing import Dict, Any

import flask
import logging

def create_app(test_config=None):
    app = flask.Flask(__name__, instance_relative_config=True)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Loading configurations...')
    if test_config is None:
        app.config.from_mapping({
            'KAFKA_BOOTSTRAP_SERVERS': os.environ['KAFKA_BOOTSTRAP_SERVERS'],
            'GROUP_NAME': os.environ.get('GROUP_NAME') or 'test-group1'
        })
    else:
        app.config.from_mapping(test_config)
    app.logger.info('Configurations loaded')

   # ensure the instance folder exists
    os.makedirs(app.instance_path)

    from .routes import task_results_receiver
    app.register_blueprint(task_results_receiver.bp)

    @app.get('/health')
    def health_check():
        return ('', 200)

    return app

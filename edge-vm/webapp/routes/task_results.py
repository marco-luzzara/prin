from typing import Generator, Any
import time
import socket
import json

from flask import (
    Blueprint, current_app, stream_template
)
from kafka import KafkaConsumer

from .middlewares.authenticated import authenticated
from ..session_wrapper import session_wrapper
from .utils.validation import validate_scope
from ..category_flash import flash_action_success
# from .. import _kafka_consumer

bp = Blueprint('task-results', __name__, url_prefix='/task-results')

## Testing results generator with:
# def get_task_results() -> Generator[Any, None, None]:
#     yield {
#         'timestamp': '2025-06-18T15:02:35',
#         'type': 'inference',
#         'filename': 'results_inf.json',
#         'url': 'http://google.it'
#     }
#     yield {
#         'timestamp': '2025-06-18T15:02:37',
#         'type': 'training',
#         'filename': 'results_tr.json',
#         'url': 'http://unimi.it'
#     }
#     time.sleep(5)
#     yield {
#         'timestamp': '2025-06-18T15:02:42',
#         'type': 'training',
#         'filename': 'results_tr.json',
#         'url': 'http://unimi.it'
#     }


@bp.get('/')
@authenticated
def view_task_results():
    # auto_offset_reset is set to earliest because the task result consumer
    # always reads from the beginning. Besides, it should not commit the message
    # offset for the same reason
    _kafka_consumer = KafkaConsumer(
        bootstrap_servers=current_app.config['KAFKA_BOOTSTRAP_SERVERS'],
        client_id=f'edge-vm-{socket.gethostname()}',
        value_deserializer=lambda m: json.loads(m.decode()),
        auto_offset_reset='earliest',
        enable_auto_commit=False
    )
    _kafka_consumer.subscribe(topics=['devprin.task.result'])

    def get_task_results() -> Generator[Any, None, None]:
        for task_result_msg in _kafka_consumer:
            task_result = task_result_msg.value
            yield {
                'timestamp': task_result['taskTimestamp'],
                'type': task_result['taskType'],
                'filename': task_result['fileName'],
                'url': task_result['preSignedUrl']
            }

    # _kafka_consumer.seek_to_beginning()

    return stream_template('task-results.html', task_results=get_task_results())

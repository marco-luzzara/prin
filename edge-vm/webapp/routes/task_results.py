from typing import Generator, Any
import time

from flask import (
    Blueprint, render_template, current_app, stream_template
)

from .middlewares.authenticated import authenticated
from ..session_wrapper import session_wrapper
from .utils.validation import validate_scope
from ..category_flash import flash_action_success
from .. import _kafka_consumer

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
def get_task_results() -> Generator[Any, None, None]:
    for task_result in _kafka_consumer:
        yield {
            'timestamp': task_result['taskTimestamp'],
            'type': task_result['taskType'],
            'fileName': task_result['fileName'],
            'url': task_result['preSignedUrl']
        }


@bp.get('/')
@authenticated
def view_task_results():
    _kafka_consumer.seek_to_beginning()

    return stream_template('task-results.html', task_results=get_task_results())

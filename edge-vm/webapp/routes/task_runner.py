import json
from flask import (
    Blueprint, render_template, current_app, request
)
from .utils.validation import validate_scope
from .. import _kafka_producer

bp = Blueprint('task-runner', __name__, url_prefix='/tasks')

@bp.get('/')
def view_task_runner_dashboard():
    return render_template('task-runner.html',
                           group_name = current_app.config['GROUP_NAME'],
                           username = current_app.config['USERNAME'])


@bp.post('/trigger')
def trigger_task():
    task_scope = request.args.get('scope', '')
    validate_scope(task_scope)

    current_app.logger.info(f'Sending notification for task {task_scope}...')
    _kafka_producer.send(
        topic="devprin.task.trigger", 
        key={ 'group_name': current_app.config['GROUP_NAME'] },
        value={ 
            'trigger_type': 'manual',
            'scope': task_scope,
            'group_name': current_app.config['GROUP_NAME'], 
            'username': current_app.config['USERNAME']
        }
    )
    _kafka_producer.flush()

    current_app.logger.info(f'Notification for task {task_scope} sent')

    return ('', 204)

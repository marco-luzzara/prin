import json

from flask import (
    Blueprint, render_template, current_app, request, redirect
)

from .middlewares.authenticated import authenticated
from ..session_wrapper import session_wrapper
from .utils.validation import validate_scope, validate_entrypoint
from ..category_flash import flash_action_success
from .. import _kafka_producer

bp = Blueprint('task-runner', __name__, url_prefix='/tasks')

@bp.get('/')
@authenticated
def view_task_runner_dashboard():
    return render_template('task-runner.html')


@bp.post('/trigger')
@authenticated
def trigger_task():
    task_scope = request.form.get('scope', '').strip()
    validate_scope(task_scope)

    task_entrypoint = request.form.get('entrypoint', '').strip()
    validate_entrypoint(task_entrypoint)
    task_entrypoint_param = ['python', 'main.py'] if task_entrypoint == '' \
        else json.loads(task_entrypoint)

    current_app.logger.info(f'Sending notification for task {task_scope}...')
    _kafka_producer.send(
        topic="devprin.task.trigger", 
        key={ 'group_name': session_wrapper.group },
        value={ 
            'trigger_type': 'manual',
            'scope': task_scope,
            'group': session_wrapper.group, 
            'user': session_wrapper.user,
            'params': {
                'entrypoint': task_entrypoint_param
            }
        }
    )
    _kafka_producer.flush()

    current_app.logger.info(f'Notification for task {task_scope} sent')
    
    flash_action_success('Il task è stato avviato correttamente')

    return redirect(request.referrer)

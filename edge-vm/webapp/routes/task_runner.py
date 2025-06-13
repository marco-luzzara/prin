from flask import (
    Blueprint, render_template, current_app, request
)

from .middlewares.authenticated import authenticated
from ..session_wrapper import session_wrapper
from .utils.validation import validate_scope
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
    task_scope = request.form.get('scope', '')
    validate_scope(task_scope)

    current_app.logger.info(f'Sending notification for task {task_scope}...')
    _kafka_producer.send(
        topic="devprin.task.trigger", 
        key={ 'group_name': session_wrapper.group },
        value={ 
            'trigger_type': 'manual',
            'scope': task_scope,
            'group': session_wrapper.group, 
            'user': session_wrapper.user
        }
    )
    _kafka_producer.flush()

    current_app.logger.info(f'Notification for task {task_scope} sent')
    
    flash_action_success('Il task è stato avviato correttamente')

    return ('', 204)

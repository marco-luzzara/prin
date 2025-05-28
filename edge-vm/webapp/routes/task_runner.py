import json
import os
import socket
from flask import (
    Blueprint, render_template, current_app, request
)
from confluent_kafka import Producer
from .utils.validation import validate_scope

bp = Blueprint('task-runner', __name__, url_prefix='/tasks')



kafka_conf = {
    'bootstrap.servers': os.environ['KAFKA_BOOTSTRAP_SERVERS'],
    'client.id': socket.gethostname()
}
producer = Producer(kafka_conf)

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
    producer.produce("devprin.task.trigger", 
        key=json.dumps({ 'group_name': current_app.config['GROUP_NAME'] }).encode(), 
        value=json.dumps({ 
            'trigger_type': 'manual',
            'scope': task_scope,
            'group_name': current_app.config['GROUP_NAME'], 
            'username': current_app.config['USERNAME']
        }).encode())

    current_app.logger.info(f'Notification for task {task_scope} sent')

    return ('', 204)

import json
import os
import socket
from flask import (
    Blueprint, render_template, current_app
)
from confluent_kafka import Producer

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


@bp.post('/trigger-inference')
def trigger_inference():
    current_app.logger.info(f'Sending notification for inference triggering...')
    producer.produce("devprin.model-inference.trigger", 
        key=json.dumps({ 'group_name': current_app.config['GROUP_NAME'] }).encode(), 
        value=json.dumps({ 
            "trigger_type": 'manual', 
            'group_name': current_app.config['GROUP_NAME'], 
            'username': current_app.config['USERNAME']
        }).encode())

    current_app.logger.info(f'Notification for inference triggering sent')
    return ('', 204)


@bp.post('/trigger-training')
def trigger_training():
    current_app.logger.info(f'Sending notification for training triggering...')
    producer.produce("devprin.model-training.trigger", 
        key=json.dumps({ 'group_name': current_app.config['GROUP_NAME'] }).encode(), 
        value=json.dumps({ 
            "trigger_type": 'manual', 
            'group_name': current_app.config['GROUP_NAME'], 
            'username': current_app.config['USERNAME']
        }).encode())

    current_app.logger.info(f'Notification for training triggering sent')
    return ('', 204)
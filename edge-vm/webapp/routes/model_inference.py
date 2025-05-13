import json
import os
import socket
from flask import (
    Blueprint, render_template, current_app
)
from confluent_kafka import Producer

bp = Blueprint('model-inference', __name__, url_prefix='/inference')

kafka_conf = {
    'bootstrap.servers': os.environ['KAFKA_BOOTSTRAP_SERVERS'],
    'client.id': socket.gethostname()
}
producer = Producer(kafka_conf)

@bp.get('/')
def view_inference_dashboard():
    return render_template('model-inference.html')


@bp.post('/trigger')
def trigger_inference():
    current_app.logger.info(f'Sending notification for inference triggering...')
    producer.produce("devprin.model-inference", 
                     key=json.dumps({ 'owner_id': current_app.config['OWNER_ID'] }).encode(), 
                     value=json.dumps({ "trigger_type": 'manual' }).encode())

    current_app.logger.info(f'Notification for inference triggering sent')
    return ('', 204)

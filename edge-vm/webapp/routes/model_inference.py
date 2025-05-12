import json
from flask import (
    Blueprint, render_template, current_app
)
from ..record_processors import KafkaProcessor

bp = Blueprint('model-inference', __name__, url_prefix='/inference')

@bp.get('/')
def view_inference_dashboard():
    return render_template('model-inference.html')


@bp.post('/trigger')
def trigger_inference():
    processor = KafkaProcessor(current_app)

    current_app.logger.info(f'Sending notification for inference triggering...')
    processor.consume("devprin.model-inference", current_app.config['OWNER_ID'], { "trigger_type": 'manual' })

    current_app.logger.info(f'Notification for inference triggering sent')
    return ('', 204)

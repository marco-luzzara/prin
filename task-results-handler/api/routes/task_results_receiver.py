import os
from typing import Any, List
from flask import (
    Blueprint, request, current_app
)
from kafka import KafkaProducer
from werkzeug.utils import secure_filename
from .utils.validation import validate_task_type

bp = Blueprint('results', __name__, url_prefix='/results')

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', '')
if KAFKA_BOOTSTRAP_SERVERS == '':
    raise Exception('Env variable KAFKA_BOOTSTRAP_SERVERS is empty')

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS
    client_id='restapi-storage-server'
)

@bp.post('/<task_type>/save')
def load_from_excel(task_type):
    task_type = task_type.strip()
    if task_type.strip() == '':
        return f'Parameter task_type cannot be blank: "{task_type}"', 400
    
    group_name: str = request.args.get('group_name', '')
    if group_name.strip() == '':
        return f'Parameter group_name cannot be blank: "{group_name}"', 400

    if len(request.files) == 0:
        return 'Received 0 files', 400

    for file_name, file in request.files.items():
        current_app.logger.info(f'Saving file {secure_filename(file_name)}...')

        file_content = file.stream.read()
        

        current_app.logger.info(f'File {secure_filename(file_name)} saved')

    return ('', 204)

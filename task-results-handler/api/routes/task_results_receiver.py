import os
from datetime import datetime
import tempfile

from boto3 import client as boto_client
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

S3_ENDPOINT = os.getenv('S3_ENDPOINT', '')
if S3_ENDPOINT == '':
    raise Exception('Env variable S3_ENDPOINT is empty')

S3_ACCESS_KEY_ID = os.getenv('S3_ACCESS_KEY_ID', '')
if S3_ACCESS_KEY_ID == '':
    raise Exception('Env variable S3_ACCESS_KEY_ID is empty')

S3_SECRET_ACCESS_KEY = os.getenv('S3_SECRET_ACCESS_KEY', '')
if S3_SECRET_ACCESS_KEY == '':
    raise Exception('Env variable S3_SECRET_ACCESS_KEY is empty')

S3_BUCKET = 'prin'

S3_PRE_SIGNED_URL_EXPIRATION_SECONDS = int(os.getenv('S3_PRE_SIGNED_URL_EXPIRATION_SECONDS'))

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    client_id='restapi-storage-server'
)

s3_client = boto_client(
    service_name='s3', 
    use_ssl=False, 
    endpoint_url=S3_ENDPOINT,
    aws_access_key_id=S3_ACCESS_KEY_ID,
    aws_secret_access_key=S3_SECRET_ACCESS_KEY
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
    
    task_timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    for file_name, file in map(lambda x: (secure_filename(x[0]), x[1]), request.files.items()):
        current_app.logger.info(f'Saving file {file_name}...')
        s3_key_for_file = generate_s3_key(
            group_name=group_name, 
            task_type=task_type, 
            task_timestamp=task_timestamp, 
            file_name=file_name
        )

        pre_signed_url = save_on_s3(file, s3_key=s3_key_for_file)

        current_app.logger.info(f'File {file_name} saved')

    return ('', 204)


def save_on_s3(file, s3_key: str) -> str:
    '''Save a file on S3 and generate a pre-signed URL for it
    '''
    with tempfile.NamedTemporaryFile() as stored_file:
        file.save(stored_file)
        s3_client.upload_file(stored_file.name, S3_BUCKET, s3_key)

    pre_signed_url = s3_client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': S3_BUCKET, 
            'Key': s3_key
        },
        ExpiresIn=S3_PRE_SIGNED_URL_EXPIRATION_SECONDS
    )

    return pre_signed_url


def generate_s3_key(group_name: str, task_type: str, task_timestamp: str, file_name: str):
    return f'{group_name}/{task_type}/{task_timestamp}/{file_name}'
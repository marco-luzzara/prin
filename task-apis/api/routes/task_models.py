import os
import json
from datetime import datetime
import tempfile

from werkzeug.datastructures import FileStorage
from boto3 import client as boto_client
from flask import (
    Blueprint, request, current_app, send_file, jsonify
)
from werkzeug.utils import secure_filename

bp = Blueprint('models', __name__, url_prefix='/models')

S3_ENDPOINT = os.getenv('S3_ENDPOINT', '')
if S3_ENDPOINT == '':
    raise Exception('Env variable S3_ENDPOINT is empty')

S3_ACCESS_KEY_ID = os.getenv('S3_ACCESS_KEY_ID', '')
if S3_ACCESS_KEY_ID == '':
    raise Exception('Env variable S3_ACCESS_KEY_ID is empty')

S3_SECRET_ACCESS_KEY = os.getenv('S3_SECRET_ACCESS_KEY', '')
if S3_SECRET_ACCESS_KEY == '':
    raise Exception('Env variable S3_SECRET_ACCESS_KEY is empty')

S3_BUCKET = os.getenv('S3_BUCKET', '')
if S3_BUCKET == '':
    raise Exception('Env variable S3_BUCKET is empty')

S3_PRE_SIGNED_URL_EXPIRATION_SECONDS = int(os.getenv('S3_PRE_SIGNED_URL_EXPIRATION_SECONDS'))

s3_client = boto_client(
    service_name='s3', 
    use_ssl=False, 
    endpoint_url=S3_ENDPOINT,
    aws_access_key_id=S3_ACCESS_KEY_ID,
    aws_secret_access_key=S3_SECRET_ACCESS_KEY
)


@bp.post('/')
def save_model():    
    group_name: str = request.args.get('group_name', '').strip()
    if group_name == '':
        return f'Parameter group_name cannot be blank: "{group_name}"', 400

    if len(request.files) != 1:
        return 'You must send exactly one file, i.e. the model to save', 400
    
    model_timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    model_file = next(request.files.values())

    current_app.logger.info(f'Saving model on S3...')
    model_s3_path = save_model_on_s3(
        file=model_file,
        group_name=group_name,
        model_timestamp=model_timestamp
    )
    current_app.logger.info(f'Model saved on S3')

    return jsonify({
        'modelPathOnS3': model_s3_path
    })


@bp.get('/<model_version>')
def get_model(model_version):
    model_version = model_version.strip()
    if model_version.strip() == '':
        return f'Parameter model_version cannot be blank: "{model_version}"', 400
    
    group_name: str = request.args.get('group_name', '').strip()
    if group_name == '':
        return f'Parameter group_name cannot be blank: "{group_name}"', 400

    with tempfile.TemporaryFile() as model_file:
        current_app.logger.info(f'Retrieving model with version {model_version} from S3...')
        get_model_from_s3(model_file, group_name, model_version)
        current_app.logger.info(f'Model with version {model_version} downloaded from S3')

        model_file.seek(0)
        return send_file(model_file)


def save_model_on_s3(
        file: FileStorage, 
        group_name: str, 
        model_timestamp: str
    ) -> str:
    '''Save the model on S3 to the following paths:
        - {group_name}/model/{model_timestamp}
        - {group_name}/model/latest
    Returns the S3 key where the model is saved
    '''

    s3_key_with_ts = generate_s3_key(
            group_name=group_name, 
            model_timestamp=model_timestamp
        )
    
    s3_key_with_latest = generate_s3_key(
            group_name=group_name, 
            model_timestamp='latest'
        )

    file.stream.seek(0)
    s3_client.upload_fileobj(
        file.stream, 
        Bucket=S3_BUCKET,
        Key=s3_key_with_ts
    )

    s3_client.delete_object(
        Bucket=S3_BUCKET,
        Key=s3_key_with_latest
    )
    file.stream.seek(0)
    s3_client.upload_fileobj(
        file.stream,
        Bucket=S3_BUCKET,
        Key=s3_key_with_latest
    )

    return s3_key_with_ts


def get_model_from_s3(model_file, group_name: str, model_version: str):
    '''Save the model retrieved from 
        s3://${S3_BUCKET}/{group_name}/model/{model_version}
    in `model_file`.
    '''

    s3_key = generate_s3_key(
            group_name=group_name, 
            model_version=model_version
        )

    s3_client.download_fileobj(S3_BUCKET, s3_key, model_file)


def generate_s3_key(group_name: str, model_version: str):
    return f'{group_name}/model/{model_version}'

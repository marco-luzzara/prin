import json
from typing import Any, List
from flask import (
    Blueprint, render_template, request, current_app
)
import pandas as pd
from werkzeug.utils import secure_filename
import dataclasses

from .model.PatientRecord import PatientRecord
from .model.utils import from_dict
from .. import _kafka_producer
from .utils.validation import validate_scope

bp = Blueprint('patients-data-loading', __name__, url_prefix='/data-loading/patients')

@bp.get('/')
def view_data_loading_dashboard():
    return render_template('patient-data-loading.html')


@bp.post('/from-excel')
def load_from_excel():
    data_file = request.files['data_file']
    task_scope = request.args.get('scope', '')
    validate_scope(task_scope)

    current_app.logger.info(f'File {secure_filename(data_file.filename)} is being processed for scope {task_scope}...')

    patient_records = cast_excel_to_objs_list(data_file.stream)
    for i, patient_record in enumerate(patient_records):
        current_app.logger.info(f'Patient {i}: {patient_record}')
        owner_id = current_app.config['GROUP_NAME']
        _kafka_producer.send(
            topic='devprin.patients', 
            key={ 'owner_id': owner_id },
            value=dataclasses.asdict(patient_record) | { 'scope': task_scope }
        )
        _kafka_producer.flush()

    current_app.logger.info(f'File {secure_filename(data_file.filename)} has been processed')

    return ('', 204)


def cast_excel_to_objs_list(readable: Any) -> List[PatientRecord]:
    df = pd.read_excel(readable, engine='calamine', dtype=str)
    return [from_dict(PatientRecord, obj) for obj in json.loads(df.to_json(orient='records'))]

import json
from typing import Any, List
import dataclasses

from flask import (
    Blueprint, render_template, request, current_app, redirect
)
import pandas as pd
from werkzeug.utils import secure_filename

from .middlewares.authenticated import authenticated
from ..session_wrapper import session_wrapper
from ..category_flash import flash_action_success
from .model.PatientRecord import PatientRecord
from .model.utils import from_dict
from .. import _kafka_producer
from .utils.validation import validate_scope

bp = Blueprint('patients-data-loading', __name__, url_prefix='/data-loading/patients')

@bp.get('/')
@authenticated
def view_data_loading_dashboard():
    return render_template('patient-data-loading.html')


@bp.post('/from-excel')
@authenticated
def load_from_excel():
    data_file = request.files['data-files']
    task_scope = request.form.get('scope', '').strip()
    validate_scope(task_scope)

    current_app.logger.info(f'File {secure_filename(data_file.filename)} is being processed for scope {task_scope}...')

    patient_records = cast_excel_to_objs_list(data_file.stream)
    for i, patient_record in enumerate(patient_records):
        current_app.logger.info(f'Patient {i}: {patient_record}')
        owner_id = session_wrapper.group
        _kafka_producer.send(
            topic='devprin.patients', 
            key={ 'owner_id': owner_id },
            value=dataclasses.asdict(patient_record) | { 'scope': task_scope }
        )
    _kafka_producer.flush()

    current_app.logger.info(f'File {secure_filename(data_file.filename)} has been processed')

    flash_action_success('I dati sono stati caricati correttamente')

    return redirect(request.referrer)


def cast_excel_to_objs_list(readable: Any) -> List[PatientRecord]:
    df = pd.read_excel(readable, engine='calamine', dtype=str)
    return [from_dict(PatientRecord, obj) for obj in json.loads(df.to_json(orient='records'))]

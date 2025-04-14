import json
from typing import Any, List
from flask import (
    Blueprint, render_template, request, url_for, current_app
)
import pandas as pd
from werkzeug.utils import secure_filename

from .model.PatientRecord import PatientRecord
from . import record_processor

bp = Blueprint('pcr-results-data-loading', __name__, url_prefix='/data-loading/pcr-results')

@bp.get('/')
def view_data_loading_dashboard():
    return render_template('pcr-results-data-loading.html')


@bp.post('from-excel')
def load_from_excel():
    data_file = request.files['data_file']
    current_app.logger.info(f'File {secure_filename(data_file.filename)} is being processed...')

    patient_records = cast_excel_to_objs_list(data_file.stream)
    for i, patient_record in enumerate(patient_records):
        current_app.logger.info(f'Patient {i}: {patient_record}')
        record_processor.consume(patient_record)

    current_app.logger.info(f'File {secure_filename(data_file.filename)} has been processed')
    return ('', 204)


def cast_excel_to_objs_list(readable: Any) -> List[PatientRecord]:
    df = pd.read_excel(readable, engine='calamine', dtype={ 
        'TELEFONO': str ,
        'DATA DI NASCITA': str,
        '1° visita': str,
        'Data diagnosi': str
    })
    return [PatientRecord.from_dict(obj) for obj in json.loads(df.to_json(orient='records'))]
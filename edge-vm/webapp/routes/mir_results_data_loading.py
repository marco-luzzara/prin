import json
from typing import Any, List
from flask import (
    Blueprint, render_template, request, current_app
)
import pandas as pd
from werkzeug.utils import secure_filename
import dataclasses

from .model.MiRRecord import MiRRecord
from .model.utils import from_dict
from .. import record_processor

bp = Blueprint('mir-results-data-loading', __name__, url_prefix='/data-loading/mir-results')

@bp.get('/')
def view_data_loading_dashboard():
    return render_template('mir-results-data-loading.html',
                           group_name = current_app.config['GROUP_NAME'],
                           username = current_app.config['USERNAME'])


@bp.post('/from-excel')
def load_from_excel():
    data_file = request.files['data_file']
    current_app.logger.info(f'File {secure_filename(data_file.filename)} is being processed...')

    mir_records = cast_excel_to_objs_list(data_file.stream)
    for i, mir_record in enumerate(mir_records):
        current_app.logger.info(f'Mir record {i}: {mir_record}')
        owner_id = current_app.config['GROUP_NAME']
        record_processor.process('devprin.mir-results', owner_id, dataclasses.asdict(mir_record))

    current_app.logger.info(f'File {secure_filename(data_file.filename)} has been processed')
    return ('', 204)


def cast_excel_to_objs_list(readable: Any) -> List[MiRRecord]:
    df = pd.read_excel(readable, engine='calamine', dtype=str)
    return [from_dict(MiRRecord, obj) for obj in json.loads(df.to_json(orient='records'))]

import json
from typing import Any, List
import dataclasses

from flask import (
    Blueprint, render_template, request, current_app, redirect
)
import pandas as pd
from werkzeug.utils import secure_filename

from .middlewares.authenticated import authenticated
from ..category_flash import flash_action_success
from ..session_wrapper import session_wrapper
from .model.MiRRecord import MiRRecord
from .model.utils import from_dict
from .. import _kafka_producer
from .utils.validation import validate_scope

bp = Blueprint('mir-results-data-loading', __name__, url_prefix='/data-loading/mir-results')

@bp.get('/')
@authenticated
def view_data_loading_dashboard():
    return render_template('mir-results-data-loading.html')


@bp.post('/from-excel')
@authenticated
def load_from_excel():
    data_file = request.files['data-files']
    task_scope = request.form.get('scope', '')
    validate_scope(task_scope)

    current_app.logger.info(f'File {secure_filename(data_file.filename)} is being processed for scope {task_scope}...')

    mir_records = cast_excel_to_objs_list(data_file.stream)
    for i, mir_record in enumerate(mir_records):
        current_app.logger.info(f'Mir record {i}: {mir_record}')
        owner_id = session_wrapper.group
        _kafka_producer.send(
            topic='devprin.mir-results', 
            key={ 'owner_id': owner_id },
            value=dataclasses.asdict(mir_record) | { 'scope': task_scope }
        )
        _kafka_producer.flush()

    current_app.logger.info(f'File {secure_filename(data_file.filename)} has been processed')

    flash_action_success('I dati sono stati caricati correttamente')

    return redirect(request.referrer)


def cast_excel_to_objs_list(readable: Any) -> List[MiRRecord]:
    df = pd.read_excel(readable, engine='calamine', dtype=str)
    return [from_dict(MiRRecord, obj) for obj in json.loads(df.to_json(orient='records'))]

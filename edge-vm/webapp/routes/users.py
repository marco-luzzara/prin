import json
from flask import (
    Blueprint, render_template, current_app, request, session
)

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.post('/login')
def login_user():
    data = request.get_json()
    group = data.get('group_name', '').strip()
    user = data.get('username', '').strip()

    current_app.config['GROUP_NAME'] = group
    current_app.config['USERNAME'] = user

    current_app.logger.info(f'Logged in as {group}:{user}')
    return ('', 204)

from flask import (
    Blueprint, redirect, current_app, request
)

from ..session_wrapper import session_wrapper
from ..category_flash import flash_action_success

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.post('/login')
def login():
    group = request.form.get('group').strip()
    user = request.form.get('user').strip()

    session_wrapper.group = group
    session_wrapper.user = user

    current_app.logger.info(f'Logged in as {group}:{user}')
    flash_action_success('Login avvenuto con successo')

    return redirect(request.referrer)


@bp.post('/logout')
def logout():
    current_app.logger.info(f'User {session_wrapper.group}:{session_wrapper.user} has logged out')
    session_wrapper.clear()

    flash_action_success('Logout avvenuto con successo')

    return redirect(request.referrer)
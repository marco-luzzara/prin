from flask import (
    Blueprint, redirect, current_app, request, flash
)

from ..session_wrapper import session_wrapper

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.post('/login')
def login():
    group = request.form.get('group').strip()
    user = request.form.get('user').strip()

    session_wrapper.group = group
    session_wrapper.user = user

    current_app.logger.info(f'Logged in as {group}:{user}')
    flash('Login avvenuto con successo', 'action_success')

    return redirect(request.referrer)


@bp.post('/logout')
def logout():
    current_app.logger.info(f'User {session_wrapper.group}:{session_wrapper.user} has logged out')
    session_wrapper.clear()

    flash('Logout avvenuto con successo', 'action_success')

    return redirect(request.referrer)
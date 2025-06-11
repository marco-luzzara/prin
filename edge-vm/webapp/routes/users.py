import json
from flask import (
    Blueprint, redirect, current_app, request, session, flash
)

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.post('/login')
def login():
    group = request.form.get('group').strip()
    user = request.form.get('user').strip()

    session['group'] = group
    session['user'] = user

    current_app.logger.info(f'Logged in as {group}:{user}')
    flash('Login avvenuto con successo', 'success')

    return redirect(request.referrer)


@bp.post('/logout')
def logout():
    current_app.logger.info(f'User {session['group']}:{session['user']} has logged out')
    flash('Logout avvenuto con successo', 'success')

    session.clear()

    return redirect(request.referrer)
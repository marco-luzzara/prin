from flask import flash

def flash_action_success(msg: str):
    flash(msg, 'action_success')


def flash_error(msg: str):
    flash(msg, 'error')
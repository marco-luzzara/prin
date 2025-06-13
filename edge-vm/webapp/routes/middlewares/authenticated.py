import functools

from flask import redirect, url_for

from ...session_wrapper import session_wrapper
from ...category_flash import flash_error


def authenticated(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if session_wrapper.user is None:
            flash_error('Per accedere alla pagina è necessario essere autenticati')

            return redirect(url_for('homepage'))

        return view(*args, **kwargs)

    return wrapped_view
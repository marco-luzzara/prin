import functools

from flask import session, has_request_context

def request_context_validated(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        if not has_request_context():
            raise Exception('Cannot access the flask.session object without a request context')
        return fn(*args, **kwargs)
    return wrapper

class SessionWrapper:
    @property
    @request_context_validated
    def user(self):
        return session.get('user', None)

    @user.setter
    @request_context_validated
    def user(self, value):
        session['user'] = value

    @property
    @request_context_validated
    def group(self):
        return session.get('group', None)

    @group.setter
    @request_context_validated
    def group(self, value):
        session['group'] = value

    def clear(self):
        session.clear()

session_wrapper = SessionWrapper()
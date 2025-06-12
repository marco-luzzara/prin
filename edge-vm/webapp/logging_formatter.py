import logging

from flask import has_request_context, request

from .session_wrapper import session_wrapper

class AuthenticatedRequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.group = session_wrapper.group or '_'
            record.user = session_wrapper.user or '_'
            record.url = request.url
        else:
            record.group = '_'
            record.user = '_'
            record.url = None

        return super().format(record)

import traceback
import logging

from flask import jsonify, request
from werkzeug.exceptions import HTTPException

from logging.handlers import RotatingFileHandler

class BaseHttpException(Exception):
    def __init__(self) -> None:
        self.code: int = 500
        self.description: str = 'Something went wrong.'


class ValidationError(BaseHttpException):
    def __init__(self, description: str):
        super().__init__()

        self.description = description
        self.code = 400


def http_exception_handler(error: BaseHttpException):
    """
        Method handle all exceptions that are inherited from BaseHttpException.
        return JSON with info about exception and write exception to logs
    """
    stack_trace = traceback.format_exc()
    logger = logging.getLogger('gunicorn.error')
    logger.exception(error.description)
    return jsonify({
        'description': error.description,
        'stack_trace': stack_trace if error.code not in [401, 403] else None,
        'request_data': request.json
    }), error.code


def python_exception_handler(error: Exception):
    """
    Method handle all exceptions that are not handled in another handlers.
    return JSON with info about exception and write exception to logs
    """
    if isinstance(error, HTTPException):
        return error

    logger = logging.getLogger('gunicorn.error')
    logger.exception('Exception handled')
    file_handler = RotatingFileHandler('logs/somelog.log', maxBytes=20240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.ERROR)
    logger.addHandler(file_handler)

    return jsonify({
        'description': 'Error handled during processing request. You can get more info from stack trace',
        'stack_trace': traceback.format_exc(),
        'request_data': request.json
    }), 500

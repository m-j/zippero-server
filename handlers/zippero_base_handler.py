import logging
import traceback

from tornado.web import RequestHandler

from errors.error_codes import ErrorCodes
from errors.errors import ZipperoError


class ZipperoBaseHandler(RequestHandler):
    def write_generic_error(self):
        self.set_status(500)
        self.finish({
            'error_code': ErrorCodes.GENERAL.value,
            'message': 'General error'
        })

    def write_error_response(self, type, err):
        self.set_header('Content-Type', 'application/json')

        if issubclass(type, ZipperoError):
            logging.error(f'Caught error {err.error_code.value} ({err.error_code.name})')

            self.set_status(status_code=err.status_code)
            self.finish(err.to_json())
        else:
            self.write_generic_error()

    def write_error(self, status_code, **kwargs):
        if 'exc_info' in kwargs:
            (type, value, _) = exc_info = kwargs['exc_info']

            self.write_error_response(type, value)
        else:
            self.write_generic_error()
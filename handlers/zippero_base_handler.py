import logging
import traceback

from tornado.web import RequestHandler

from errors.error_codes import ErrorCodes
from errors.errors import ZipperoError


class ZipperoBaseHandler(RequestHandler):
    def write_error(self, status_code, **kwargs):
        if 'exc_info' in kwargs:
            self.set_header('Content-Type', 'application/json')
            (type, value, _) = exc_info = kwargs['exc_info']

            if issubclass(type, ZipperoError):
                err: ZipperoError = value
                logging.error(f'Caught error {err.error_code.value} ({err.error_code.name})')

                self.set_status(status_code=err.status_code)
                self.finish(err.to_json())
            else:
                self.set_status(500)
                self.finish({
                    'error_code': ErrorCodes.GENERAL.value,
                    'message': 'General error'
                })
        else:
            self.set_status(status_code)
            self.finish({
                'error_code': ErrorCodes.GENERAL.value,
                'message': 'General error'
            })
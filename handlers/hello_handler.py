from jsonschema import validate
from tornado import escape
from tornado.web import HTTPError

from handlers.zippero_base_handler import ZipperoBaseHandler
from errors.errors import TestError, UnauthorizedError
from security.privilege_validator import PrivilegeValidator

global_repo = [
    {'id': 1, 'code': 'dupa'}
]

last_id = 1

schema = {
    'type': 'object',
    'properties': {
        'id': {'type' : 'number'},
        'code': {'type': 'string'}
    }
}

class HelloHandler(ZipperoBaseHandler):
    _privilege_validator: PrivilegeValidator

    def initialize(self, privilege_validator: PrivilegeValidator):
        self._privilege_validator = privilege_validator

    async def get(self):
        if not self._privilege_validator.validate_request_readonly(self.request):
            raise UnauthorizedError()

        raise TestError()

        host = self.request.headers.get('Host')
        self.write(host)

    async def post(self):
        body = self.request.body
        payload = escape.json_decode(body)

        validate(payload, schema)

        global_repo.append(payload)
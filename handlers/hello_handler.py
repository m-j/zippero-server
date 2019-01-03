from jsonschema import validate
from tornado import escape
from tornado.web import RequestHandler, HTTPError

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

class HelloHandler(RequestHandler):
    _privilege_validator: PrivilegeValidator

    def initialize(self, privilege_validator: PrivilegeValidator):
        self._privilege_validator = privilege_validator

    async def get(self):
        if not self._privilege_validator.validate_request_readonly(self.request):
            raise HTTPError(status_code=401, log_message='This endpoint requires readonly or readwrite key')

        host = self.request.headers.get('Host')
        self.write(host)

    async def post(self):
        body = self.request.body
        payload = escape.json_decode(body)

        validate(payload, schema)

        global_repo.append(payload)
from jsonschema import validate
from tornado import escape
from tornado.web import RequestHandler

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
    async def get(self):
        host = self.request.headers.get('Host')
        self.write(host)

    async def post(self):
        body = self.request.body
        payload = escape.json_decode(body)

        validate(payload, schema)

        global_repo.append(payload)
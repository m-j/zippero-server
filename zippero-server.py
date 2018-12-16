from jsonschema import validate
from tornado import ioloop, web, escape

from package_management.data_scanner import scan_data_directory
from utils import load_config

config = load_config.load_config()

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

class HelloHandler(web.RequestHandler):
    async def get(self):
         self.finish({'entries': global_repo})

    async def post(self):
        body = self.request.body
        payload = escape.json_decode(body)

        validate(payload, schema)

        global_repo.append(payload)


def create_tornado_app():
    return web.Application([
        (r'/hello', HelloHandler),
    ])

def start_server():
    app = create_tornado_app()
    app.listen(port=config['server']['port'])
    ioloop.IOLoop.current().start()

def main():
    scan_data_directory(config['repository']['dataFolder'])

if __name__ == '__main__':
    main()


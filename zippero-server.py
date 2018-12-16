from jsonschema import validate
from tornado import ioloop, web, escape

from handlers.hello_handler import HelloHandler
from handlers.packages_hanler import PackagesHandler
from package_management.data_scanner import scan_data_directory
from utils import load_config

config = load_config.load_config()


def create_tornado_app():
    return web.Application([
        (r'/hello', HelloHandler),
        (r'/packages', PackagesHandler)
    ])

def start_server():
    app = create_tornado_app()
    app.listen(port=config['server']['port'])
    ioloop.IOLoop.current().start()

def main():
    # scan_data_directory(config['repository']['dataFolder'])
    start_server()

if __name__ == '__main__':
    main()


from jsonschema import validate
from tornado import ioloop, web, escape

from handlers.hello_handler import HelloHandler
from handlers.package_info_handler import PackageInfoHandler
from handlers.packages_handler import PackagesHandler

from package_management.package_manager import PackageManager
from utils import load_config

config = load_config.load_config()


def create_tornado_app():
    package_manager = PackageManager(config['repository']['dataFolder'])
    package_manager.scan()

    return web.Application([
        (r'/hello', HelloHandler),
        (r'/package-info/(?P<package_name>[^/]+)', PackageInfoHandler, {'package_manager': package_manager}),
        (r'/packages', PackagesHandler, {'package_manager': package_manager})
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


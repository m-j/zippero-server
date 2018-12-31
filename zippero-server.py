import logging

from jsonschema import validate
from tornado import ioloop, web, escape

from handlers.get_packages_handler import GetPackagesHandler
from handlers.hello_handler import HelloHandler
from handlers.package_info_handler import PackageInfoHandler
from handlers.add_packages_handler import AddPackagesHandler

from package_management.package_manager import PackageManager
from package_management.paths_util import PathsUtil
from utils import load_config

config = load_config.load_config()

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

def create_tornado_app():
    data_folder = config['repository']['dataFolder']
    paths_util = PathsUtil(data_folder)
    package_manager = PackageManager(data_folder, paths_util)
    package_manager.scan()

    return web.Application([
        (r'/hello', HelloHandler),
        (r'/package-info/(?P<package_name>[^/]+)', PackageInfoHandler, {'package_manager': package_manager}),
        (r'/packages', AddPackagesHandler, {'package_manager': package_manager}),
        (r'/packages/(?P<name>[^/]+)/(?P<version>[^/]+)', GetPackagesHandler, {'package_manager': package_manager})
    ])


async def started_callback(port):
    logging.info(f'Zippero server started and listening on port {port}')


def start_server():
    app = create_tornado_app()
    port = config['server']['port']
    app.listen(port=port)
    ioloop.IOLoop.current().add_callback(started_callback, port)
    ioloop.IOLoop.current().start()


def main():
    start_server()

if __name__ == '__main__':
    main()


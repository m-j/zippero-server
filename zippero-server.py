import logging
from logging.handlers import RotatingFileHandler

from tornado import ioloop, web

from handlers.add_packages_handler import AddPackagesHandler
from handlers.get_packages_handler import GetPackagesHandler
from handlers.hello_handler import HelloHandler
from handlers.package_info_handler import PackageInfoHandler
from package_management.package_manager import PackageManager
from package_management.paths_util import PathsUtil
from security.privilege_validator import PrivilegeValidator
from utils import load_config
import os

config = load_config.load_config()


def setup_logging():
    logger = logging.getLogger()
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] - %(message)s")

    logger.setLevel(logging.DEBUG)

    logs_folder = config['logsFolder']
    os.makedirs(logs_folder, exist_ok=True)

    file_handler = RotatingFileHandler(
        os.path.join(logs_folder, 'zippero-server.log'),
        maxBytes=1024*1024*10,
        backupCount=3)

    file_handler.formatter = formatter

    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.formatter = formatter

    logger.addHandler(stream_handler)


def create_tornado_app():
    data_folder = config['repository']['dataFolder']
    privilege_validator = PrivilegeValidator()
    privilege_validator.load_keys(config['keys'])

    paths_util = PathsUtil(data_folder)
    package_manager = PackageManager(data_folder, paths_util)
    package_manager.scan()

    return web.Application([
        (r'/hello', HelloHandler, {'privilege_validator': privilege_validator}),
        (r'/package-info/(?P<package_name>[^/]+)', PackageInfoHandler, {
            'package_manager': package_manager, 'privilege_validator': privilege_validator
        }),
        (r'/packages', AddPackagesHandler, {
            'package_manager': package_manager, 'privilege_validator': privilege_validator
        }),
        (r'/packages/(?P<name>[^/]+)/(?P<version>[^/]+)', GetPackagesHandler, {
            'package_manager': package_manager, 'privilege_validator': privilege_validator
        })
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
    setup_logging()
    start_server()

if __name__ == '__main__':
    main()


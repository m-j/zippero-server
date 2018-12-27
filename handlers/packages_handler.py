from tornado.httputil import HTTPFile
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler
import tempfile

from package_management.errors import PackageAlreadExistsError
from package_management.package_manager import PackageManager


def save_file_body_to_temporary_file(b: bytes) -> str:
    # todo check how big files behave. look at streaming
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(b)
        return tmp.name


async def save_file_body_to_temporary_file_async(b: bytes) -> str:
    return await IOLoop.current().run_in_executor(None, save_file_body_to_temporary_file, b)


class PackagesHandler(RequestHandler):
    package_manager: PackageManager

    def initialize(self, package_manager):
        self.package_manager = package_manager

    async def post(self):
        file: HTTPFile = self.request.files['package'][0]

        try:
            self.clear()
            temp_file_path = await save_file_body_to_temporary_file_async(file['body'])
            await self.package_manager.add_package(temp_file_path)
            self.set_status(201)
        except PackageAlreadExistsError as ex:
            self.set_status(400)
            self.write(f'Package {ex.package_name} in version {ex.package_version} already exists')
        finally:
            self.finish()
from tornado.httputil import HTTPFile
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler
import tempfile

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

        temp_file_path = await save_file_body_to_temporary_file_async(file['body'])
        await self.package_manager.add_package(temp_file_path)

        # 1. receive temp file
        # 2. read metadata file, parse it and store it in mem
        # 3. craete appropriate diractories structure for package version
        # 4. move temp file to new directory and create metadata file

        self.clear()
        self.set_status(201)
        self.finish()
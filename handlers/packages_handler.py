import re

import aiofiles
import tornado
from aiofiles.base import AiofilesContextManager
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


def create_new_tempfile() -> str:
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        return tmp.name

async def save_file_body_to_temporary_file_async(b: bytes) -> str:
    return await IOLoop.current().run_in_executor(None, save_file_body_to_temporary_file, b)

def parse_content_params(chunk: bytes, boundary: bytes):
    chunk.re

@tornado.web.stream_request_body
class PackagesHandler(RequestHandler):
    package_manager: PackageManager
    _file: AiofilesContextManager
    _temp_file_path: str = None
    _boundary: str = None

    def initialize(self, package_manager):
        self.package_manager = package_manager

    def prepare(self):
        self.request.connection.set_max_body_size(1024**3)
        content_type = self.request.headers.get('Content-Type')
        print(content_type)

    async def data_received(self, chunk):
        if not self._temp_file_path:
            self._temp_file_path = create_new_tempfile()

        async with aiofiles.open(self._temp_file_path, 'ab') as file:
            await file.write(chunk)

    async def post(self):
        if not self._temp_file_path:
            self.set_status(400)
            self.write('No file data provided')
        try:
            self.clear()
            temp_file_path = self._temp_file_path
            await self.package_manager.add_package(temp_file_path)
            self.set_status(201)
        except PackageAlreadExistsError as ex:
            self.set_status(400)
            self.write(f'Package {ex.package_name} in version {ex.package_version} already exists')
        finally:
            self.finish()
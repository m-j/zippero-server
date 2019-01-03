import logging
from time import time
from typing import Optional

import aiofiles
import tornado
from aiofiles.base import AiofilesContextManager
from tornado.web import RequestHandler
import tempfile

from errors.errors import PackageAlreadExistsError
from handlers.zippero_base_handler import ZipperoBaseHandler
from package_management.package_manager import PackageManager

# ----- Benchmark -----
# Opening file each part: Body processed in 24.232001066207886s
# Opening onece: Body processed in 2.949439764022827s
from security.privilege_validator import PrivilegeValidator


def create_new_tempfile() -> str:
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        return tmp.name

@tornado.web.stream_request_body
class AddPackagesHandler(ZipperoBaseHandler):
    _privilege_validator: PrivilegeValidator
    _package_manager: PackageManager
    _file: AiofilesContextManager
    _temp_file_path: Optional[str] = None
    _start_time = None

    def initialize(self, package_manager, privilege_validator: PrivilegeValidator):
        self._package_manager = package_manager
        self._privilege_validator = privilege_validator

    async def prepare(self):
        self._privilege_validator.assure_readwrite_access(self.request)

        self.request.connection.set_max_body_size(1024**3)
        content_type = self.request.headers.get('Content-Type')
        print(content_type)
        self._start_time = time()
        self._temp_file_path = create_new_tempfile()
        self._file = await aiofiles.open(self._temp_file_path, 'ab')

    async def data_received(self, chunk):
        try:
            await self._file.write(chunk)
        except:
            await self._file.close()
            self._file = None
            raise

    async def post(self):
        if self._file:
            await self._file.close()

        logging.info(f'Body prcessed in {(time() - self._start_time)}s')

        if not self._temp_file_path:
            self.set_status(400)
            self.write('No file data provided')
            logging.info('No file data provided. Unable to upload package')
        try:
            self.clear()
            temp_file_path = self._temp_file_path
            await self._package_manager.add_package(temp_file_path)
            self.set_status(201)
        except PackageAlreadExistsError as ex:
            self.set_status(400)
            self.write(f'Package {ex.package_name} in version {ex.package_version} already exists')
            self.info(f'Package {ex.package_name} in version {ex.package_version} already exists')
        finally:
            self.finish()
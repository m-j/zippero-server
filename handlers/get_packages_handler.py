from tornado.web import RequestHandler

from handlers.zippero_base_handler import ZipperoBaseHandler
from package_management.package_manager import PackageManager
from security.privilege_validator import PrivilegeValidator


async def generator():
    for i in range(5):
        yield f'--{i}--'

class GetPackagesHandler(ZipperoBaseHandler):
    _privilege_validator: PrivilegeValidator
    _package_manager: PackageManager

    def initialize(self, package_manager, privilege_validator: PrivilegeValidator):
        self._package_manager = package_manager
        self._privilege_validator = privilege_validator

    async def get(self, name, version):
        self._privilege_validator.assure_readonly_access(self.request)

        async for chunk_bytes in self._package_manager.read_package(name, version):
            self.add_header('Content-Type', 'application/zip')
            self.write(chunk_bytes)

        self.finish()

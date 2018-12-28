from tornado.web import RequestHandler

from package_management.package_manager import PackageManager


class GetPackagesHandler(RequestHandler):
    _package_manager: PackageManager

    def initialize(self, package_manager):
        self._package_manager = package_manager

    async def get(self, name, version):
        self.write(f'here it {name}@{version}')
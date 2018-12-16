from tornado.web import RequestHandler

from handlers.handler_utils import wrap_in_envelope
from package_management.package_manager import PackageManager


class PackagesHandler(RequestHandler):
    package_manager: PackageManager

    def initialize(self, package_manager):
        self.package_manager = package_manager

    async def get(self):
        packages = self.package_manager.query(package_name='test.packageA')
        self.finish(wrap_in_envelope(packages))

        # todo: This endpoint should be returning list of objects with links
        # todo: Metadata and actual zip files should be separate concepts


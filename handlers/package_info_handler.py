from tornado.web import RequestHandler

from handlers.handler_utils import wrap_in_envelope
from package_management.package_manager import PackageManager


class PackageInfoHandler(RequestHandler):
    package_manager: PackageManager

    def initialize(self, package_manager):
        self.package_manager = package_manager

    async def get(self, package_name):
        package_info = self.package_manager.query(package_name=package_name)

        if package_info is not None:
            self.finish(wrap_in_envelope(package_info.as_dict()))
        else:
            self.send_error(404)

        # todo: This endpoint should be returning list of objects with links
        # todo: Metadata and actual zip files should be separate concepts


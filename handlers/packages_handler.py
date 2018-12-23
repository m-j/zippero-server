from tornado.web import RequestHandler

from package_management.package_manager import PackageManager


class PackagesHandler(RequestHandler):
    package_manager: PackageManager

    def initialize(self, package_manager):
        self.package_manager = package_manager

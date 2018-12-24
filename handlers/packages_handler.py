from tornado.httputil import HTTPFile
from tornado.web import RequestHandler
import tempfile

from package_management.package_manager import PackageManager


class PackagesHandler(RequestHandler):
    package_manager: PackageManager

    def initialize(self, package_manager):
        self.package_manager = package_manager

    async def post(self):
        file: HTTPFile = self.request.files['package'][0]

        await self.package_manager.add_package(file['body'])

        self.clear()
        self.set_status(201)
        self.finish()
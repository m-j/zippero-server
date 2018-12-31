from tornado.web import RequestHandler

from handlers.handler_utils import wrap_in_envelope
from package_management.package_manager import PackageManager
from package_management.utils import package_link


class PackageInfoHandler(RequestHandler):
    package_manager: PackageManager

    def initialize(self, package_manager):
        self.package_manager = package_manager

    async def get(self, package_name):
        package_info = self.package_manager.query(name=package_name)

        if package_info is not None:
            package_info_dict = self.make_package_info_dict(package_info)
            self.finish(wrap_in_envelope(package_info_dict))
        else:
            self.send_error(404)

    def make_package_info_dict(self, package_info):
        package_info_dict = package_info.as_dict()
        host = self.request.headers.get('Host')
        package_info_dict['links'] = {version: package_link(self.request.protocol, host, package_info.name, version) for
                                      version in package_info.versions}

        return package_info_dict




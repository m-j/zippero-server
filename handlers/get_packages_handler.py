from tornado.web import RequestHandler

from package_management.package_manager import PackageManager

async def generator():
    for i in range(5):
        yield f'--{i}--'

class GetPackagesHandler(RequestHandler):
    _package_manager: PackageManager

    def initialize(self, package_manager):
        self._package_manager = package_manager

    async def get(self, name, version):
        async for num in generator():
            self.write(num)

        self.finish()

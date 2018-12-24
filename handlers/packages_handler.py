from tornado.web import RequestHandler
import tempfile

from package_management.package_manager import PackageManager


class PackagesHandler(RequestHandler):
    package_manager: PackageManager

    def initialize(self, package_manager):
        self.package_manager = package_manager

    def post(self):
        file = self.request.files['package'][0]
        original_filename = file['filename']

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(file['body'])
            print(f'file uploaded: {tmp.name}')

        self.clear()
        self.set_status(201)
        self.finish()
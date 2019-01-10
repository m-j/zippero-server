from typing import Optional

from errors.error_codes import ErrorCodes
from package_management.utils import fullname


class ZipperoError(Exception):
    error_code: ErrorCodes = ErrorCodes.GENERAL
    message: str = 'General exception'
    status_code: int = 500

    def to_json(self):
        return {
            'error_code': self.error_code.value,
            'message': self.message
        }


class PackageAlreadyExistsError(ZipperoError):
    package_name: str
    package_version: str
    status_code: int = 400
    error_code = ErrorCodes.PACKAGE_ALREADY_EXISTS

    def __init__(self, package_name: str, package_version: str):
        self.package_version = package_version
        self.package_name = package_name
        self.message = f'Package {fullname(package_name, package_version)} already exists'


class PackageDoesntExistError(ZipperoError):
    package_name: str
    package_version: str
    status_code: int = 404
    error_code = ErrorCodes.PACKAGE_DOESNT_EXIST

    def __init__(self, package_name: str, package_version: str):
        self.package_name = package_name
        self.package_version = package_version
        self.message = f'Package {fullname(package_name, package_version)} does not exist'


class UnauthorizedError(ZipperoError):
    def __init__(self, message='Unauthorized'):
        self.message = message

    error_code = ErrorCodes.UNAUTHORIZED
    message = 'Unauthorized'
    status_code = 401


class TestError(ZipperoError):
    test_message: str


class MaliciousDataError(ZipperoError):
    error_code = ErrorCodes.MALICIOUS_DATA
    status_code = 400
    message = 'Malicious data attempt detected'

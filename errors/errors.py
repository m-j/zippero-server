from typing import Optional

from errors.error_codes import ErrorCodes


class ZipperoError(Exception):
    error_code: ErrorCodes = ErrorCodes.GENERAL
    message: str = 'General exception'
    status_code: int = 500

    def to_json(self):
        return {
            'error_code': self.error_code.value,
            'message': self.message
        }


class PackageAlreadExistsError(ZipperoError):
    package_name: str
    package_version: str
    status_code: int = 400

    def __init__(self, package_name: str, package_version: str):
        self.package_version = package_version
        self.package_name = package_name


class PackageDoesntExistError(ZipperoError):
    package_name: str
    package_version: str
    status_code: int = 404

    def __init__(self, package_name: str, package_version: str):
        self.package_name = package_name
        self.package_version = package_version


class UnauthorizedError(ZipperoError):
    def __init__(self, message='Unauthorized'):
        self.message = message

    error_code = ErrorCodes.UNAUTHORIZED
    message = 'Unauthorized'
    status_code = 401


class TestError(ZipperoError):
    test_message: str


class MaliciousDataError(ZipperoError):
    pass
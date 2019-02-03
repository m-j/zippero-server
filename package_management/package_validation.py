import re

from errors.errors import InvalidNameError, InvalidVersionError

version_regex = r'^[\.\d]+$'
name_regex = r'^[\w\.\-]+$'


def validate_package_name(name: str):
    m = re.match(name_regex, name)
    if m is None:
        raise InvalidNameError(name)


def validate_package_version(version: str):
    m = re.match(version_regex, version)
    if m is None:
        raise InvalidVersionError(version)

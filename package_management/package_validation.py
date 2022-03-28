import re

from errors.errors import InvalidNameError, InvalidVersionError

# Semantic versioning: https://semver.org/
# https://regex101.com/r/Ly7O1x/3/
version_regex = r'^(0|[1-9]\d*)\.(0|[1-9]\d*)\.([0-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$'
name_regex = r'^[\w\.\-]+$'


def validate_package_name(name: str):
    m = re.match(name_regex, name)
    if m is None:
        raise InvalidNameError(name)


def validate_package_version(version: str):
    m = re.match(version_regex, version)
    if m is None:
        raise InvalidVersionError(version)

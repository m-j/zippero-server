class ZipperoError(Exception):
    pass


class PackageAlreadExistsError(ZipperoError):
    package_name: str
    package_version: str

    def __init__(self, package_name: str, package_version: str):
        self.package_version = package_version
        self.package_name = package_name


class PackageDoesntExistError(ZipperoError):
    package_name: str
    package_version: str

    def __init__(self, package_name: str, package_version: str):
        self.package_name = package_name
        self.package_version = package_version
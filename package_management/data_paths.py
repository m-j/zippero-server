import os

packages = 'packages'


def get_packages_path(data_directory: str):
    return os.path.join(data_directory, packages)
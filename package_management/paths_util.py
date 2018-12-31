import os
import pathlib
from typing import List

from package_management import data_paths
from package_management.constants import zpspec_filename


class PathsUtil:
    _data_dir_path: str

    def __init__(self, data_dir_path: str):
        self._data_dir_path = data_dir_path

    def get_package_version_zpspec_path(self, name, version):
        return os.path.join(self.get_package_version_dir_path(name, version), zpspec_filename)

    def get_package_version_file_path(self, name: str, version: str):
        return os.path.join(self.get_package_version_dir_path(name, version), f'{name}.zip')

    def get_package_version_dir_path(self, name, version):
        return os.path.join(self._data_dir_path, data_paths.packages, name, version)

    def path_is_valid(self, path: str):
        pathlib_path_to_validate = pathlib.Path(os.path.abspath(path))
        pathlib_data_dir = pathlib.Path(os.path.abspath(os.path.join(self._data_dir_path, data_paths.packages)))

        return pathlib_data_dir in pathlib_path_to_validate.parents

    def paths_are_valid(self, paths: List[str]):
        for path in paths:
            if not self.path_is_valid(path):
                return False

        return True
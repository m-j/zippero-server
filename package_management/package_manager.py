import copy

from package_management.data_scanning import scan_data_directory


class PackageManager:
    _data_dir_path: str
    _packages_dict: dict

    def __init__(self, data_dir_path: str):
        self._data_dir_path = data_dir_path

    def scan(self):
        packages_dict = scan_data_directory(self._data_dir_path)
        # todo: validate integirty here in a future
        self._packages_dict = packages_dict

    def query(self, package_name: str = None, version: str = None):
        if(package_name is not None):
            return copy.deepcopy(self._packages_dict[package_name])
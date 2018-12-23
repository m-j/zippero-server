import copy
from dataclasses import dataclass, asdict
from typing import List, Dict
from package_management.data_scanning import scan_data_directory
from package_management.model import PackageMetadata, PackageInfo


def packages_metadata_from_versions(name: str, semvers: List[str]):
    return [PackageMetadata(name=name, semver=semver) for semver in semvers]


class PackageManager:
    _data_dir_path: str
    _package_infos: Dict[str, List[PackageInfo]]

    def __init__(self, data_dir_path: str):
        self._data_dir_path = data_dir_path

    def scan(self):
        package_infos = scan_data_directory(self._data_dir_path)
        # todo: validate integirty here in a future
        self._package_infos = package_infos

    def query(self, package_name: str = None, version: str = None) -> PackageInfo:
        if package_name is not None:
            return copy.deepcopy(self._package_infos[package_name])
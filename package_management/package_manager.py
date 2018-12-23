import copy
from dataclasses import dataclass, asdict
from typing import List, Dict
from package_management.data_scanning import scan_data_directory


@dataclass(frozen=True)
class PackageMetadata:
    name: str
    semver: str

    def as_dict(self):
        d = asdict(self)
        return d


def packages_metadata_from_versions(name: str, semvers: List[str]):
    return [PackageMetadata(name=name, semver=semver) for semver in semvers]


class PackageManager:
    _data_dir_path: str
    _packages: Dict[str, List[PackageMetadata]]

    def __init__(self, data_dir_path: str):
        self._data_dir_path = data_dir_path

    def scan(self):
        packages_dict = scan_data_directory(self._data_dir_path)
        # todo: validate integirty here in a future
        packages_metadata = {name: packages_metadata_from_versions(name, versions) for (name, versions) in packages_dict.items()}
        self._packages = packages_metadata

    def query(self, package_name: str = None, version: str = None):
        if package_name is not None:
            return copy.deepcopy(self._packages[package_name])
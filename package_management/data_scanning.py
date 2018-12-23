import os
from typing import List, Dict

import package_management.data_paths as data_paths
from package_management.model import PackageInfo


def list_versions_in_package_folder(package_folder: str):
    version_dirs = os.listdir(package_folder)
    return version_dirs


def build_package_info(name: str, versions: List[str]):
    return PackageInfo(name, versions, links=None)


def scan_data_directory(data_dir_path: str) -> Dict[str, PackageInfo]:
    packages_path = data_paths.get_packages_path(data_dir_path)
    package_folders = os.listdir(packages_path)

    packages_dict = {package_name:
                         list_versions_in_package_folder(os.path.join(data_dir_path, data_paths.packages, package_name))
                     for package_name in package_folders}

    package_info_dicts = {name: build_package_info(name=name, versions=versions) for (name, versions) in
                          packages_dict.items()}

    return package_info_dicts

import copy
import json
import logging
import os
import shutil
from threading import Lock
from typing import List, Dict, Optional
from zipfile import ZipFile

import aiofiles
from tornado.ioloop import IOLoop

from package_management import data_paths
from package_management.constants import zpspec_filename, package_name_key, version_key
from package_management.data_scanning import scan_data_directory
from package_management.errors import PackageAlreadExistsError, PackageDoesntExistError
from package_management.model import PackageMetadata, PackageInfo
from package_management.utils import fullname

read_chunk_size = 1024*1024*10

def packages_metadata_from_versions(name: str, semvers: List[str]):
    return [PackageMetadata(name=name, semver=semver) for semver in semvers]


def parse_zpfile(temp_file_path: str):
    with ZipFile(temp_file_path) as zip_file:
        print(zip_file.namelist())
        zpspec_contents = zip_file.read(zpspec_filename)
        json_dict = json.loads(zpspec_contents, encoding='UTF-8')
        return json_dict


class PackageManager:
    _data_dir_path: str
    _package_infos: Dict[str, PackageInfo]
    _packages_in_processing_fullnames: List[str]
    _package_infos_lock: Lock

    def __init__(self, data_dir_path: str):
        self._data_dir_path = data_dir_path
        self._packages_in_processing_fullnames = []
        self._package_infos_lock = Lock()

    def scan(self):
        package_infos = scan_data_directory(self._data_dir_path)
        # todo: validate integirty here in a future
        self._package_infos = package_infos

    def query(self, name: str = None) -> Optional[PackageInfo]:
        if name is None:
            raise ValueError('You have to provide package name')

        if name in self._package_infos:
            package_info = self._package_infos[name]
            return package_info
        else:
            return None

    def add_package_sync(self, temp_file_path: str):
        json_dict = parse_zpfile(temp_file_path)

        name = json_dict[package_name_key]
        version = json_dict[version_key]

        package_version_dir_path = self._get_package_version_dir_path(name, version)
        package_version_file_path = self._get_package_version_file_path(name, version)
        package_version_zpspec_path = self._get_package_version_zpspec_path(name, version)

        self._add_fullname_to_in_processing_or_raise_exception(name, version)

        try:
            try:
                os.makedirs(package_version_dir_path, exist_ok=False)
            except OSError as err:
                raise PackageAlreadExistsError(package_name=name, package_version=version)

            shutil.move(temp_file_path, package_version_file_path)
            # what if we fail here? it will violate integrity
            with open(package_version_zpspec_path, mode='wt') as zpspec_file:
                json.dump(json_dict, zpspec_file)

            with self._package_infos_lock:
                self._add_version_to_package_info(name, version)

            logging.info(f'Successfully added new package: {fullname(name, version)}')

        finally:
            with self._package_infos_lock:
                self._packages_in_processing_fullnames.remove(fullname(name, version))

    def _get_package_version_zpspec_path(self, name, version):
        return os.path.join(self._get_package_version_dir_path(name, version), zpspec_filename)

    def _get_package_version_file_path(self, name: str, version: str):
        return os.path.join(self._get_package_version_dir_path(name, version), f'{name}.zip')

    def _get_package_version_dir_path(self, name, version):
        return os.path.join(self._data_dir_path, data_paths.packages, name, version)

    def _add_version_to_package_info(self, name, version):
        if name not in self._package_infos:
            package_infos_clone = copy.deepcopy(self._package_infos)
            package_infos_clone[name] = PackageInfo(name=name, versions=[], links=None)
            package_infos_clone[name].versions.append(version)
            self._package_infos = package_infos_clone

    def _add_fullname_to_in_processing_or_raise_exception(self, name, version):
        with self._package_infos_lock:
            if name in self._package_infos and version in self._package_infos[name].versions:
                raise PackageAlreadExistsError(package_name=name, package_version=version)

            if fullname(name, version) in self._packages_in_processing_fullnames:
                raise PackageAlreadExistsError(package_name=name, package_version=version)

            self._packages_in_processing_fullnames.append(fullname(name, version))

    async def add_package(self, temp_file_path: str):
        return await IOLoop.current().run_in_executor(None, self.add_package_sync, temp_file_path)

    async def read_package(self, name: str, version: str):
        if name is None or version is None:
            raise ValueError('You have to specify both name and version')

        # todo: protect from deleting package when it is being read

        package_info = self.query(name=name)

        if (package_info is None) or (version not in package_info.versions):
            raise PackageDoesntExistError(name, version)

        package_file_path = self._get_package_version_file_path(name, version)

        # todo: try-catch

        async with aiofiles.open(package_file_path, mode='rb') as file:
            while True:
                chunk_bytes = await file.read(read_chunk_size)
                if len(chunk_bytes) > 0:
                    yield chunk_bytes
                else:
                    return


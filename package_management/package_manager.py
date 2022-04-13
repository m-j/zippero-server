import copy
import json
import logging
import os
import shutil
from distutils.version import LooseVersion
from threading import Lock
from typing import List, Dict, Optional
from zipfile import ZipFile

import aiofiles
from tornado.ioloop import IOLoop

from package_management.constants import zpspec_filename, package_name_key, version_key
from package_management.data_scanning import scan_data_directory
from errors.errors import PackageAlreadyExistsError, PackageDoesntExistError, MaliciousDataError
from package_management.model import PackageMetadata, PackageInfo
from package_management.package_validation import validate_package_name, validate_package_version
from package_management.paths_util import PathsUtil
from package_management.utils import fullname

read_chunk_size = 3*1024*1024*10


def packages_metadata_from_versions(name: str, semvers: List[str]):
    return [PackageMetadata(name=name, semver=semver) for semver in semvers]


def parse_zpfile(temp_file_path: str):
    with ZipFile(temp_file_path) as zip_file:
        print(zip_file.namelist())
        zpspec_contents = zip_file.read(zpspec_filename)
        json_dict = json.loads(zpspec_contents)
        return json_dict


class PackageManager:
    _paths_util: PathsUtil
    _data_dir_path: str
    _package_infos: Dict[str, PackageInfo]
    _packages_in_processing_fullnames: List[str]
    _package_infos_lock: Lock

    def __init__(self, data_dir_path: str, paths_util: PathsUtil):
        self._paths_util = paths_util
        self._data_dir_path = data_dir_path
        self._packages_in_processing_fullnames = []
        self._package_infos_lock = Lock()

    def scan(self):
        package_infos = scan_data_directory(self._data_dir_path)
        # todo: validate integirty here in a future
        self._package_infos = package_infos

    def query_all(self) -> Dict[str, PackageInfo]:
        return self._package_infos

    def query(self, name: str) -> Optional[PackageInfo]:
        if name is None:
            raise ValueError('You have to provide package name')

        if name in self._package_infos:
            package_info = self._package_infos[name]
            return package_info
        else:
            return None

    def remove_package_sync(self, package_name: str, package_version: str):
        validate_package_name(package_name)
        validate_package_version(package_version)

        package_version_dir_path = self._paths_util.get_package_version_dir_path(package_name, package_version)
        try:
            dir_exists = os.path.isdir(package_version_dir_path)
            if dir_exists:
                print('Removing package ' + package_name + ' in version ' + package_version)
                shutil.rmtree(package_version_dir_path)
            with self._package_infos_lock:
                self._remove_version_to_package_info(package_name, package_version)

            logging.info(f'Successfully removed package: {fullname(package_name, package_version)}')
        except OSError as err:
            logging.error(f'Error occurred while removing package: {fullname(package_name, package_version)}!')

    def add_package_sync(self, temp_file_path: str):
        json_dict = parse_zpfile(temp_file_path)

        name = json_dict[package_name_key]
        version = json_dict[version_key]

        validate_package_name(name)
        validate_package_version(version)

        package_version_dir_path = self._paths_util.get_package_version_dir_path(name, version)
        package_version_file_path = self._paths_util.get_package_version_file_path(name, version)
        package_version_zpspec_path = self._paths_util.get_package_version_zpspec_path(name, version)

        if not self._paths_util.paths_are_valid([package_version_dir_path, package_version_file_path, package_version_zpspec_path]):
            logging.error(f'Tried to create package in folder {package_version_dir_path} which is outside data directory')
            raise MaliciousDataError()

        self._add_fullname_to_in_processing_or_raise_exception(name, version)

        try:
            try:
                os.makedirs(package_version_dir_path, exist_ok=False)
            except OSError as err:
                raise PackageAlreadyExistsError(package_name=name, package_version=version)

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

    def _add_version_to_package_info(self, name, version):
        package_infos_clone = copy.deepcopy(self._package_infos)

        if name not in self._package_infos:
            package_infos_clone[name] = PackageInfo(name=name, versions=[])

        package_infos_clone[name].versions.append(version)
        package_infos_clone[name].versions.sort(key=LooseVersion)
        self._package_infos = package_infos_clone

    def _remove_version_to_package_info(self, name, version):
        package_infos_clone = copy.deepcopy(self._package_infos)

        if name not in self._package_infos:
            package_infos_clone[name] = PackageInfo(name=name, versions=[])

        package_infos_clone[name].versions.remove(version)
        package_infos_clone[name].versions.sort(key=LooseVersion)

        if len(package_infos_clone[name].versions) == 0:
            del package_infos_clone[name]

        self._package_infos = package_infos_clone

    def _add_fullname_to_in_processing_or_raise_exception(self, name, version):
        with self._package_infos_lock:
            if name in self._package_infos and version in self._package_infos[name].versions:
                raise PackageAlreadyExistsError(package_name=name, package_version=version)

            if fullname(name, version) in self._packages_in_processing_fullnames:
                raise PackageAlreadyExistsError(package_name=name, package_version=version)

            self._packages_in_processing_fullnames.append(fullname(name, version))

    async def add_package(self, temp_file_path: str):
        return await IOLoop.current().run_in_executor(None, self.add_package_sync, temp_file_path)

    async def remove_package(self, package_name: str, package_version: str):
        return await IOLoop.current().run_in_executor(None, self.remove_package_sync, package_name, package_version)

    async def read_package(self, name: str, version: str):
        if name is None or version is None:
            raise ValueError('You have to specify both name and version')

        # todo: protect from deleting package when it is being read

        package_info = self.query(name=name)

        if (package_info is None) or (version not in package_info.versions):
            raise PackageDoesntExistError(name, version)

        package_file_path = self._paths_util.get_package_version_file_path(name, version)

        if not self._paths_util.path_is_valid(package_file_path):
            logging.error(f'Tried to read data from file {package_file_path} which is outside data directory')
            raise MaliciousDataError()

        try:
            async with aiofiles.open(package_file_path, mode='rb') as file:
                while True:
                    chunk_bytes = await file.read(read_chunk_size)
                    if len(chunk_bytes) > 0:
                        yield chunk_bytes
                    else:
                        return
        except OSError as oserr:
            logging.exception(f'Failed to open file {package_file_path} for reading')
            raise PackageDoesntExistError(name, version)



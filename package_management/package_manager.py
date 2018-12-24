import copy
import tempfile
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional

from tornado.httputil import HTTPFile
from tornado.ioloop import IOLoop

from package_management.data_scanning import scan_data_directory
from package_management.model import PackageMetadata, PackageInfo


def packages_metadata_from_versions(name: str, semvers: List[str]):
    return [PackageMetadata(name=name, semver=semver) for semver in semvers]


def save_file_body_to_temporary_file(b: bytes) -> str:
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(b)
        return tmp.name


class PackageManager:
    _data_dir_path: str
    _package_infos: Dict[str, PackageInfo]

    def __init__(self, data_dir_path: str):
        self._data_dir_path = data_dir_path

    def scan(self):
        package_infos = scan_data_directory(self._data_dir_path)
        # todo: validate integirty here in a future
        self._package_infos = package_infos

    def query(self, package_name: str = None, version: str = None) -> Optional[PackageInfo]:
        if package_name is not None:
            if package_name in self._package_infos:
                package_info = self._package_infos[package_name]
                return copy.deepcopy(package_info)
            else:
                return None
        else:
            raise ValueError('Wrong parameter')

    def _add_package_sync(self, body: bytes):
        temp_file_path = save_file_body_to_temporary_file(body)
        print(temp_file_path)

    async def add_package(self, body: bytes):
        await IOLoop.current().run_in_executor(None, self._add_package_sync, body)




from package_management.package_manager import PackageManager
from package_management.paths_util import PathsUtil


class RetentionManager:
    _data_dir_path: str
    _max_number_of_packages_per_versions: int
    _package_manager: PackageManager

    def __init__(self, data_dir_path: str, max_number_of_packages_per_versions: str):
        self._data_dir_path = data_dir_path
        self._max_number_of_packages_per_versions = int(max_number_of_packages_per_versions)
        self._package_manager = PackageManager(data_dir_path, PathsUtil(data_dir_path))

    def clean(self):
        self._package_manager.scan()
        all_packages = self._package_manager.query_all()
        for key in all_packages:
            if len(all_packages[key].versions) > self._max_number_of_packages_per_versions:
                end_idx = len(all_packages[key].versions) - self._max_number_of_packages_per_versions
                for version in reversed(all_packages[key].versions[0:end_idx]):
                    self._package_manager.remove_package_sync(key, version)

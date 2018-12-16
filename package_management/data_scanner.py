import os
import package_management.data_paths as data_paths

def list_versions_in_package_folder(package_folder: str):
    version_dirs = os.listdir(package_folder)
    return version_dirs

def scan_data_directory(data_dir_path: str):
    packages_path = data_paths.get_packages_path(data_dir_path)
    package_folders = os.listdir(packages_path)

    packages_dict = {package_name:
                         list_versions_in_package_folder(os.path.join(data_dir_path, data_paths.packages,package_name))
                     for package_name in package_folders}

    print(packages_dict)

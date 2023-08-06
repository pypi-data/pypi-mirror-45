#!/usr/bin/env python3

from pathlib import Path


def get_folder_size(path: Path) -> int:
    """
    Get size of the folder (folder and files).
    :param path: Path: Path.

    """
    return sum([file.stat().st_size for file in path.glob("**/*")])


def get_folders_size(path: Path) -> int:
    """
    Get size of folders in path.
    :param path: Path: Path.

    """
    return sum([file.stat().st_size for file in path.glob("**")])


def get_files_size(path: Path) -> int:
    """
    Get size of files (but not folders) in path.
    :param path: Path: Path.

    """
    return get_folder_size(path) - get_folders_size(path)

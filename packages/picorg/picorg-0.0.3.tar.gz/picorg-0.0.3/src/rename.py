import os
import glob
import pathlib

from typing import List

import timestamp_finder


def rename_files(root: str = ".") -> None:
    for file in _list_files(root):
        rename_file(file)


def rename_file(file) -> None:
    exif_name = timestamp_finder.get_timestamp(file)
    if exif_name is None:
        _handle_no_exif_found(file)
    else:
        new_filename = _find_new_filename(file, exif_name)
        if new_filename != file:
            os.rename(file, new_filename)


def _list_files(root: str) -> List[str]:
    types = [".jpg"]
    result = []
    for filename in glob.glob(os.path.join(root, "**"), recursive=True):
        _, ext = os.path.splitext(filename)
        if ext.lower() in types:
            result.append(filename)
    return result


def _find_new_filename(file: str, exif_name: str) -> str:
    filepath = pathlib.Path(file)
    if filepath.name.startswith(exif_name):
        return file
    suggested_path = pathlib.Path(filepath.parent, exif_name + filepath.suffix.lower())
    if not suggested_path.is_file():
        return str(suggested_path)
    for suffix in range(1, 10 ** 5):
        suggested_path = suggested_path.with_name(
            exif_name + "(" + str(suffix) + ")" + filepath.suffix.lower()
        )
        if not suggested_path.is_file():
            return str(suggested_path)


def _handle_no_exif_found(file: str) -> None:
    filepath = pathlib.Path(file)
    if filepath.parent.name == "NOK":
        return
    new_filepath = pathlib.Path(filepath.parent, "NOK", filepath.name)
    new_filepath.parent.mkdir(exist_ok=True)
    filepath.rename(new_filepath)
    print("File NOK: {}".format(file))


if __name__ == "__main__":
    rename_files()

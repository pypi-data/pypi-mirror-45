import sys
import os
import settings


def find_duplicates():
    paths = settings.get("pic_paths", [])
    exclude_extensions = settings.get("exclude_extensions", [])
    files = {}
    for path in paths:
        files_in_path = [
            (f, os.path.join(dp, f))
            for dp, dn, filenames in os.walk(path)
            for f in filenames
            if not f.endswith(tuple(exclude_extensions))
        ]
        # Collect all files and add them with the filename as key
        for item in files_in_path:
            if item[0] not in files:
                files[item[0]] = []
            files[item[0]].append(item[1])
    # Present duplicates
    duplicates = {k: v for k, v in files.items() if len(v) > 1}
    for k, v in duplicates.items():
        print(k + " -> " + str(v))
    return 0 if len(duplicates) == 0 else -1


if __name__ == "__main__":
    sys.exit(find_duplicates())

import datetime
import os
import time
import sys

import timestamp_finder


def get_next_filename_with_counter(original_filename):
    print("Finding new name for file...")
    suffix = 1
    while True:
        filename_split = os.path.splitext(original_filename)
        new_suggestion = filename_split[0] + "(" + str(suffix) + ")" + filename_split[1]
        if not os.path.isfile(new_suggestion):
            print("New filename found! " + new_suggestion)
            return new_suggestion
        suffix = suffix + 1


def create_dirs(dirs):
    for d in dirs:
        if not os.path.exists(d):
            os.makedirs(d)


def do_work():
    create_dirs(["NOK", "OK"])
    included_extensions = ["jpg", "png", "JPG", "PNG"]
    for filename in os.listdir("."):
        if any(filename.endswith(ext) for ext in included_extensions):
            new_filename = timestamp_finder.get_timestamp(filename)
            if new_filename is None:
                print("Could not find any exif data for image: " + filename)
                if not os.path.isfile("NOK/" + filename):
                    os.rename(filename, "NOK/" + filename)
                else:
                    print("File already exists: " + "NOK/" + filename)
                continue
            filename_split = os.path.splitext(filename)
            file_extension = filename_split[1]
            if not os.path.isfile("OK/" + new_filename + file_extension):
                os.rename(filename, "OK/" + new_filename + file_extension)
            else:
                print("File already exists: " + "OK/" + new_filename + file_extension)
                filename_with_counter = get_next_filename_with_counter(
                    "OK/" + new_filename + file_extension
                )
                os.rename(filename, filename_with_counter)


if __name__ == "__main__":
    do_work()

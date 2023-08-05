from flask import send_file
import os


def return_file(save_location, file):
    """
    Opens or downloads the file if the file exists.

    :param save_location: The location within the project the user saved the files to
    :param file: The name of the file the user wishes to retrieve
    :return: The saved file or None

    >>> return_file('./content/files/', 'example.txt')

    """
    file_path = os.path.abspath(save_location + file)
    if os.path.exists(file_path):
        return send_file(file_path)
    else:
        return None

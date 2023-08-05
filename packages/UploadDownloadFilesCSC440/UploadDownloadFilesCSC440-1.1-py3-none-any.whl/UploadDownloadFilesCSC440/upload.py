import os
import werkzeug


def files_saved(save_location, files_list):
    """
    Saves the files to a specified location and returns all the names of the files currently saved in that location.

    :param save_location: The location within the project the user wishes to save the files
    :param files_list: The files uploaded by the user
    :return: A list of all the files currently saved specified location

    >>> files_saved('./content/files/', ['example.txt'])
    []
    """
    file_folder = os.path.abspath(save_location)
    # Checks that the files folder exists and creates it if it doesn't
    if not os.path.exists(file_folder):
        os.makedirs(file_folder)
    # Goes through each file uploaded by the user
    for f in files_list:
        # Checks if f is a file
        if type(f) == werkzeug.datastructures.FileStorage:
            # Retrieves the string name of the file
            filename = f.filename
            # Determines where and under what name the file is savedd
            destination = save_to(filename, file_folder)
            # Saves the file to the file folder
            f.save(destination)

    files_name_list = []
    for filename in os.listdir(file_folder):
        files_name_list.append(filename)
    return files_name_list


def save_to(filename, file_folder):
    """
    Gets the full path of where the file will be stored including the file name. This is done by figuring out if
    there is an existing file with the same name as the current file. If there is not a file with the same name it
    will return file_folder with the file named added to the end of the path. If there is file that has the same
    name it will figure out what version number should be added to the name. It will then return the file_folder
    with the revised name added to the end of the path

    :param filename: The full name including the file type
    :param file_folder: The file path for where the file will be stored
    :return: The full path of where the file will be stored including the file name

    >>> save_to('example7.txt', 'Wiki/content/files')
    'Wiki/content/files/example7.txt'
    """
    # Adds the original name to the file path
    destination = "/".join([file_folder, filename])
    # Checks if the file name already exists
    if os.path.exists(destination):
        # Gets the first version of the file name
        first_version_filename = get_first_version_filename(filename)
        # Adds the first version name to the file path
        first_version_destination = "/".join([file_folder, first_version_filename])
        # Checks if the first version of the file name already exists
        if os.path.exists(first_version_destination):
            highest_version = 0
            # Go through each file in the files folder
            for current in os.listdir(file_folder):
                # Gets the file name and current type
                file_name, current_type = get_file_name_and_type(filename)
                # Gets the current file name without the version
                current_filename_without_version = get_filename_without_version(current)
                # Determines if the current file name without the version is the same as the file name
                if current_filename_without_version == file_name:
                    # Gets the current files version number
                    version_number = get_version_number(current)
                    # Makes sure the version number is a digit
                    if version_number.isdigit():
                        # Determines if the highest version is less or equal to the version number
                        if highest_version <= int(version_number):
                            # Sets highest_version to the new version number plus 1
                            highest_version = int(version_number) + 1
                            # Gets the updated file name with the new version
                            newest_version_filename = get_newest_version_filename(filename, highest_version)
            # Returns the file path and the updated file name with the new version
            return "/".join([file_folder, newest_version_filename])

        # Returns the file path and the first version of the file name
        return first_version_destination

    # Returns the file path and the original name
    return destination


def get_first_version_filename(filename):
    """
    Gets the the first version of the full file name including the type. By first version I mean the first time the
    name has to be altered by version.

    :param filename: The full name including the file type
    :return: The new full file name including the type

    >>> get_first_version_filename('example6[1].docx')
    'example6[1][1].docx'
    """
    file_name, file_type = get_file_name_and_type(filename)
    return file_name + "[1]" + file_type


def get_version_number(filename):
    """
    Gets the version number in a file name. If there is no version number in the file name then it returns 0.

    :param filename: The full name including the file type
    :return: the string of the version number

    >>> get_version_number('example5[4378].pptx')
    '4378'
    """
    file_name, file_type = get_file_name_and_type(filename)
    open_bracket_index, closing_bracket_index = get_open_bracket_and_closing_bracket_index(file_name)
    if open_bracket_index == -1 and closing_bracket_index == -1:
        return '0'
    return file_name[(open_bracket_index + 1): closing_bracket_index]


def get_filename_without_version(filename):
    """
    Gets the file name without the version if there is a version. If there is no version in the file name it returns
    the original file name.

    :param filename: The full file name including the file type
    :return: the file name without the version

    >>> get_filename_without_version('example4[32838].pdf')
    'example4'
    """
    file_name, file_type = get_file_name_and_type(filename)
    open_bracket_index, closing_bracket_index = get_open_bracket_and_closing_bracket_index(file_name)
    if open_bracket_index != -1 and closing_bracket_index != -1:
        file_name = file_name[:open_bracket_index]
    return file_name


def get_newest_version_filename(filename, version_number):
    """
    Gets the newest version of the filename by taking the current filename and changing it to include a version of
    file.

    :param filename: The full file name including the file type
    :param version_number: An integer for
    :return: The new file name that includes the version

    >>> get_newest_version_filename('example3.jpg', 32)
    'example3[32].jpg'
    """
    file_name, file_type = get_file_name_and_type(filename)
    return file_name + "[" + str(version_number) + "]" + file_type


def get_file_name_and_type(filename):
    """
    Gets the file name and the file type.

    :param filename: The file name with the file type
    :return: file name without the file type, file type

    >>> get_file_name_and_type('example.png')
    ('example', '.png')
    """
    split_index = filename.rfind('.')
    return filename[:split_index], filename[split_index:]


def get_open_bracket_and_closing_bracket_index(file_name):
    """
    Gets the indexes for the opening bracket and the closing bracket.

    :param file_name: The file name without the file type
    :return: index for the open bracket, index for the closing bracket

    >>> get_open_bracket_and_closing_bracket_index('example2[5]')
    (8, 10)
    """
    return file_name.rfind('['), file_name.rfind(']')

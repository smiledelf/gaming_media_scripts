import os
import stat
import time
import datetime


def main():
    """
    Main function to allow the user to pick which naming scheme they want
    """

    # # Warnings
    # print("-----------------------!! WARNING !!---------------------------"
    #       "\nThis script will rename image files in the current folder!"
    #       "\nThere is no undo function available."
    #       "\n-----------------------!! WARNING !!---------------------------"
    #       "\nAre you sure you want to proceed? Type y/n: ")

    # usr = str(input()).lower()
    # if usr == 'y' or usr == 'yes':
    #     # Pick screenshot renaming scheme
    #     print("-----------------------"
    #           "\nSelect naming scheme..."
    #           "\n-----------------------"
    #           "\n1: Windows "
    #           "\n   e.g 2020-01-29 (8)"
    #           "\n2: Steam "
    #           "\n   e.g 1172470_20200129203829_8")
    #     scheme = input("Please enter the number of the naming scheme to be used: ").strip()
    #     if scheme == "1":
    #         rename_windows()
    #         ExitMethods.finished()
    #     elif scheme == "2":
    #         rename_steam()
    #         ExitMethods.finished()
    #     else:
    #         ExitMethods.invalid()

    # elif usr == 'n' or usr == 'no':
    #     ExitMethods.normal_exit()
    # else:
    #     ExitMethods.invalid()

    debug = True
    if debug:
        test_folder = "test_screenshots" # <--- change here
        script_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), test_folder)
    else:
        # set cwd to location of the script
        script_directory = os.path.dirname(os.path.abspath(__file__))
    
    os.chdir(script_directory) 

    apply_windows_naming(script_directory, True)


def get_files_to_rename(directory_path:str) -> dict:
    """
    For all files in the directory, generate a mapping between old files and new files
    - Decide whether a file should be renamed or not (e.g rename if .png)
    - Handles edge case where multiple old files was going to map to the same new file

    :param directory_path: the absolute path to the directory containing files to rename
    :return: a mapping dictionary, where {old filepath: new filepath}
    """

    # for each file in current folder, if applicable, propose a new filename (based on scheme) --> create a mapping dict. out of this?
    files_to_rename = {} # old_filepath: new_filepath
    for file in os.listdir(directory_path):

        # get file extension
        try:
            file_extension = os.path.splitext(file)[1] # e.g .png - note the '.' is included
        except IndexError as error:
            msg = f"Index error when getting file extension for file: {file}. If file has no extension, ignore this message."
            print(msg)

        if file_extension in StandardVariables.accepted_extensions:
            # extract the most recent modification date for the file, then format as string according to formatting rules
            filepath = os.path.join(directory_path, file)
            modified_timestamp = os.stat(filepath)[stat.ST_MTIME]
            modified_datetime = datetime.datetime.fromtimestamp(modified_timestamp)

            modified_datetime_formatted = modified_datetime.strftime(StandardVariables.windows_datetime_formatting)  # e.g '2020-01-29'
                    
            # TODO: branch off here depending on naming scheme - for now, Windows :)
            # propose new filename and add duplicate suffix if appropriate
            proposed_filename = f"{modified_datetime_formatted}{file_extension}"
            proposed_filepath = os.path.join(directory_path, proposed_filename)

            # handle edge case of renaming multiple old files to the same proposed filename
            # - extra logic: if in files_to_skip, it will exist so we need to take that into account too
            duplicate_index = 0
            duplicate_exists = os.path.isfile(proposed_filepath) or proposed_filepath in files_to_rename.values()
            while duplicate_exists:
                duplicate_index += 1
                proposed_filename = f"{modified_datetime_formatted} ({duplicate_index}){file_extension}"  # e.g '2020-01-29 (1).png'
                proposed_filepath = os.path.join(directory_path, proposed_filename)
                duplicate_exists = os.path.isfile(proposed_filepath) or proposed_filepath in files_to_rename.values()

            # record mapping between old filepath and proposed filepath
            files_to_rename[filepath] = proposed_filepath

    return files_to_rename


def apply_windows_naming(directory_path:str, dry_run:bool=True):
    """
    The goal: pass in a folder path, and rename based on naming scheme - output renamed files as log.

    Important edge cases:
    - Sometimes not all files need to be renamed (e.g if we already ran the script once before)

    Standards:
    - File paths - should all be in absolute full paths, especially if returning

    """

    # tbh this function should just be 'loop over files, if it matches the dict, then rename it'
    # this function currently handles most of the logic already

    files_to_rename = get_files_to_rename(directory_path) # TODO: different naming schemes?
    for filepath, proposed_filepath in files_to_rename.items():

        if dry_run:
            print(f"(Dry run) | {os.path.basename(filepath):20} ------> {os.path.basename(proposed_filepath):20}")
        else:
            try:
                os.rename(filepath, proposed_filepath)
            except FileExistsError:
                print("ERROR: Cannot rename", filepath, "to", proposed_filepath + "! File already exists.")


def rename_windows():
    """
    This naming scheme loops through the current folder and looks for image files, then
    renames them according to most recent date of modification without duplicates.

    Format is YYYY-MM-DD (N)

    Note: Time of most recent content modification is more reliable than day of creation
    Note2: Only recognises jpg and png (most common extensions) at the moment
    """

    print("----------------------------------"
          "\nRenaming using the Windows scheme!"
          "\n----------------------------------")

    # Setting up: extensions and dictionary for month conversion (e.g Jun -> 06)
    accepted_extensions = StandardVariables.accepted_extensions
    month_dict = StandardVariables.months

    # (ARGH IT'S SO BAD) Loop through current directory and find files with already-correct naming scheme
    already_correct = find_existing_windows()

    # Get current directory, then loop through its files to find which ones are screenshots
    current_directory = os.curdir

    for file in os.listdir(current_directory):
        file_extension = file[-4:]
        if (file not in already_correct) and (file_extension in accepted_extensions):

            # Extract date of most recent content modification
            filepath = os.path.join(os.curdir, file)
            filestatobject = os.stat(filepath)

            # Extract most recent modification date and split into variables
            # Note: ctime() returns a string from the datetime object
            modified_datetime = time.ctime(filestatobject[stat.ST_MTIME]).split()  # e.g [Mon, Jul, 8, 01:16:44, 2019]
            modified_day = "{:02d}".format(int(modified_datetime[2]))
            modified_month = month_dict.get(str(modified_datetime[1]))
            modified_year = str(modified_datetime[-1])
            duplicate_index = 0

            # Propose a possible filename and add duplicate index if appropriate
            # e.g 2019-06-26 (1)
            proposed_filename = modified_year + '-' + modified_month + '-' + modified_day + file_extension
            duplicate_exist = os.path.isfile(proposed_filename)  # T if dupe exists, F otherwise
            while duplicate_exist:
                duplicate_index += 1
                proposed_filename = modified_year + '-' + modified_month + '-' + modified_day + ' (' + str(
                    duplicate_index) + ")" + file_extension
                duplicate_exist = os.path.isfile(proposed_filename)

            # Rename the file to proposed filename
            try:
                os.rename(filepath, proposed_filename)
            except FileExistsError:
                print("ERROR: Cannot rename", filepath, "to", proposed_filename + "! File already exists.")
                input("Pausing the program...")


def find_existing_windows():
    """
    Modified version of the rename_windows function, used to find which pictures in the folder
    already has correct naming.

    Differences in code will be highlighted by comments in CAPITAL LETTERS.

    Output: a Python set containing filenames with already-correct naming scheme
    """

    # Known filenames will go here
    already_correct = set()

    # Setting up: extensions and dictionary for month conversion (e.g Jun -> 06)
    accepted_extensions = StandardVariables.accepted_extensions
    month_dict = StandardVariables.months

    # Get current directory, then loop through its files to find which ones are screenshots
    current_directory = os.curdir
    for file in os.listdir(current_directory):
        file_extension = file[-4:]
        if file_extension in accepted_extensions:
            # If file is a picture, extract date of most recent content modification
            filepath = os.path.join(os.curdir, file)
            filestatobject = os.stat(filepath)

            # Extract most recent modification date and split into variables
            # Note: ctime() returns a string from the datetime object
            modified_datetime = time.ctime(filestatobject[stat.ST_MTIME]).split()  # e.g [Mon, Jul, 8, 01:16:44, 2019]
            modified_day = "{:02d}".format(int(modified_datetime[2]))
            modified_month = month_dict.get(str(modified_datetime[1]))
            modified_year = str(modified_datetime[-1])
            duplicate_index = 0

            # Propose a possible filename and add duplicate index if appropriate
            # e.g 2019-06-26 (1)
            proposed_filename = modified_year + '-' + modified_month + '-' + modified_day + file_extension
            duplicate_exist = os.path.isfile(proposed_filename)  # T if dupe exists, F otherwise
            while duplicate_exist:
                already_correct.add(proposed_filename)  # ADD TO SET OF KNOWN CORRECT FILENAMES
                duplicate_index += 1
                proposed_filename = modified_year + '-' + modified_month + '-' + modified_day + ' (' + str(
                    duplicate_index) + ")" + file_extension
                duplicate_exist = os.path.isfile(proposed_filename)

            # REMOVED RENAMING TRY/EXCEPT

    return already_correct  # RETURN SET


def rename_steam():
    """
        This naming scheme loops through the current folder and looks for image files, then
        renames them according to most recent date of modification without duplicates.

        Format is AppID_YYYYMMDDHHMMSS_N.extension

        Note: Time of most recent content modification is more reliable than day of creation
        Note2: Only recognises jpg and png (most common extensions) at the moment
        """

    print("----------------------------------"
          "\nRenaming using the Steam scheme!"
          "\n----------------------------------")

    app_id = str(input("Please enter the AppID: "))
    while not app_id.isdigit():
        app_id = str(input("AppID must be an integer! Please enter the AppID: "))

    # Setting up: extensions and dictionary for month conversion (e.g Jun -> 06)
    accepted_extensions = StandardVariables.accepted_extensions
    month_dict = StandardVariables.months

    # (ARGH IT'S SO BAD) Loop through current directory and find files with already-correct naming scheme
    already_correct = find_existing_steam(app_id)

    # Get current directory, then loop through its files to find which ones are screenshots
    current_directory = os.curdir

    for file in os.listdir(current_directory):
        file_extension = file[-4:]
        if (file not in already_correct) and (file_extension in accepted_extensions):
            # Extract date of most recent content modification
            filepath = os.path.join(os.curdir, file)
            filestatobject = os.stat(filepath)

            # Extract most recent modification date and split into variables
            # Note: ctime() returns a string from the datetime object
            modified_datetime = time.ctime(filestatobject[stat.ST_MTIME]).split()  # e.g [Mon, Jul, 8, 01:16:44, 2019]
            modified_time = modified_datetime[3].replace(":", "")
            modified_day = "{:02d}".format(int(modified_datetime[2]))
            modified_month = month_dict.get(str(modified_datetime[1]))
            modified_year = str(modified_datetime[-1])
            duplicate_index = 1

            # Propose a possible filename and add duplicate index if appropriate
            # e.g 1172470_20200129203829_1
            proposed_filename = app_id + '_' + modified_year + modified_month + \
                                modified_day + modified_time + '_' + \
                                str(duplicate_index) + file_extension
            duplicate_exist = os.path.isfile(proposed_filename)  # T if dupe exists, F otherwise
            while duplicate_exist:
                duplicate_index += 1
                proposed_filename = app_id + '_' + modified_year + \
                                    modified_month + modified_day + modified_time + '_' + \
                                    str(duplicate_index) + file_extension
                duplicate_exist = os.path.isfile(proposed_filename)

            # Rename the file to proposed filename
            try:
                os.rename(filepath, proposed_filename)
            except FileExistsError:
                print("ERROR: Cannot rename", filepath, "to", proposed_filename + "! File already exists.")


def find_existing_steam(app_id):
    """
    Modified version of the rename_steam function, used to find which pictures in the folder
    already has correct naming.

    Differences in code will be highlighted by comments in CAPITAL LETTERS.

    Output: a Python set containing filenames with already-correct naming scheme
    """

    # Known filenames will go here
    already_correct = set()

    # Setting up: extensions and dictionary for month conversion (e.g Jun -> 06)
    accepted_extensions = StandardVariables.accepted_extensions
    month_dict = StandardVariables.months

    # Get current directory, then loop through its files to find which ones are screenshots
    current_directory = os.curdir
    for file in os.listdir(current_directory):
        file_extension = file[-4:]
        if file_extension in accepted_extensions:
            # If file is a picture, extract date of most recent content modification
            filepath = os.path.join(os.curdir, file)
            filestatobject = os.stat(filepath)

            # Extract most recent modification date and split into variables
            # Note: ctime() returns a string from the datetime object
            modified_datetime = time.ctime(filestatobject[stat.ST_MTIME]).split()  # e.g [Mon, Jul, 8, 01:16:44, 2019]
            modified_time = modified_datetime[3].replace(":", "")
            modified_day = "{:02d}".format(int(modified_datetime[2]))
            modified_month = month_dict.get(str(modified_datetime[1]))
            modified_year = str(modified_datetime[-1])
            duplicate_index = 1

            # Propose a possible filename and add duplicate index if appropriate
            # e.g 1172470_20200129203829_1
            proposed_filename = app_id + '_' + modified_year + modified_month + \
                                modified_day + modified_time + '_' + \
                                str(duplicate_index) + file_extension
            duplicate_exist = os.path.isfile(proposed_filename)  # T if dupe exists, F otherwise
            while duplicate_exist:
                already_correct.add(proposed_filename)  # ADD TO SET OF KNOWN CORRECT FILENAMES
                duplicate_index += 1
                proposed_filename = app_id + '_' + modified_year + modified_month + \
                                    modified_day + modified_time + '_' + \
                                    str(duplicate_index) + file_extension
                duplicate_exist = os.path.isfile(proposed_filename)

            # REMOVED RENAMING TRY/EXCEPT

    return already_correct  # RETURN SET


class StandardVariables:
    """ Class that defines the standards for frequently-used variables, such as a list of accepted extensions
    """

    accepted_extensions = [".jpg", ".png", ".bmp"]
    months = {
        "Jan": "01",
        "Feb": "02",
        "Mar": "03",
        "Apr": "04",
        "May": "05",
        "Jun": "06",
        "Jul": "07",
        "Aug": "08",
        "Sep": "09",
        "Oct": "10",
        "Nov": "11",
        "Dec": "12",
    }
    windows_datetime_formatting = "%Y-%m-%d" # e.g 2020-01-29
    steam_datetime_formatting = "%Y%m%d%H%M%S" # e.g 20200129203829


class ExitMethods:
    @staticmethod
    def finished():
        input("Finished! Press ENTER to exit...")
        exit()

    @staticmethod
    def normal_exit():
        input("Press ENTER to exit...")
        exit()

    @staticmethod
    def invalid():
        input("Invalid response!"
              "\nPress ENTER to exit...")
        exit()


if __name__ == "__main__":

    main()

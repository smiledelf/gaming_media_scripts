import os
import stat
import time


def main():
    """
    Main function to allow the user to pick which naming scheme they want
    """

    # Give user some warning
    print("-----------------------!! WARNING !!---------------------------"
          "\nThis script will rename any files that start with 'Screenshot'!"
          "\nThere is no undo function available."
          "\n-----------------------!! WARNING !!---------------------------"
          "\nAre you sure you want to proceed? Type y/n below:")

    usr = str(input()).lower()
    if usr == 'y' or usr == 'yes':
        # User entered YES - pick screenshot renaming scheme
        print("-----------------------"
              "\nSelect naming scheme..."
              "\n-----------------------"
              "\n1: Windows "
              "\n   e.g 2020-01-29 (8)"
              "\n2: Steam "
              "\n   e.g 1172470_20200129203829_8")
        scheme = input("Please enter the number: ").strip()
        if scheme == "1":
            screenshot_windows()
            input("Finished! Press ENTER to exit...")
        elif scheme == "2":
            screenshot_steam()
            input("Finished! Press ENTER to exit...")
        else:
            print("Invalid response!")
            pause = input("Press ENTER to exit...")
            exit()

    elif usr == 'n' or usr == 'no':
        pause = input("Press ENTER to exit...")
        exit()
    else:
        print("Invalid response!")
        pause = input("Press ENTER to exit...")
        exit()


def screenshot_windows():
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
    accepted_extensions = [".jpg", ".png"]
    month_dict = {
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

    # (ARGH IT'S SO BAD) Loop through current directory and find files with already-correct naming scheme
    already_correct = screenshot_windows_existing()

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
            modified_time = time.ctime(filestatobject[stat.ST_MTIME]).split()  # e.g [Mon, Jul, 8, 01:16:44, 2019]
            modified_day = "{:02d}".format(int(modified_time[2]))
            modified_month = month_dict.get(str(modified_time[1]))
            modified_year = str(modified_time[-1])
            duplicate_index = 0

            # Propose a possible filename and add duplicate index if appropriate
            # e.g 2019-06-26 (1)
            proposed_filename = modified_year + '-' + modified_month + '-' + modified_day + file_extension
            duplicate_exist = os.path.isfile(proposed_filename)  # T if dupe exists, F otherwise
            while duplicate_exist:
                duplicate_index += 1
                proposed_filename = modified_year + '-' + modified_month + '-' + modified_day + ' (' + str(duplicate_index) + ")" + file_extension
                duplicate_exist = os.path.isfile(proposed_filename)

            # Rename the file to proposed filename
            try:
                os.rename(filepath, proposed_filename)
            except FileExistsError:
                print("ERROR: Cannot rename", filepath, "to", proposed_filename + "! File already exists.")


def screenshot_windows_existing():
    """
    Modified version of the screenshot_windows function, used to find which pictures in the folder
    already has correct naming.

    Differences will be highlighted by comments in CAPITAL LETTERS.

    Output: a Python set containing filenames with already-correct naming scheme
    """

    # Known filenames will go here
    already_correct = set()

    # Setting up: extensions and dictionary for month conversion (e.g Jun -> 06)
    accepted_extensions = [".jpg", ".png"]
    month_dict = {
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
            modified_time = time.ctime(filestatobject[stat.ST_MTIME]).split()  # e.g [Mon, Jul, 8, 01:16:44, 2019]
            modified_day = "{:02d}".format(int(modified_time[2]))
            modified_month = month_dict.get(str(modified_time[1]))
            modified_year = str(modified_time[-1])
            duplicate_index = 0

            # Propose a possible filename and add duplicate index if appropriate
            # e.g 2019-06-26 (1)
            proposed_filename = modified_year + '-' + modified_month + '-' + modified_day + file_extension
            duplicate_exist = os.path.isfile(proposed_filename)  # T if dupe exists, F otherwise
            while duplicate_exist:
                already_correct.add(proposed_filename)  # ADD TO SET OF KNOWN CORRECT FILENAMES
                duplicate_index += 1
                proposed_filename = modified_year + '-' + modified_month + '-' + modified_day + ' (' + str(duplicate_index) + ")" + file_extension
                duplicate_exist = os.path.isfile(proposed_filename)

    return already_correct


def screenshot_steam():
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

    # Setting up: extensions and dictionary for month conversion (e.g Jun -> 06)
    accepted_extensions = [".jpg", ".png"]
    month_dict = {
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

    # (ARGH IT'S SO BAD) Loop through current directory and find files with already-correct naming scheme
    already_correct = screenshot_windows_existing()

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
            modified_time = time.ctime(filestatobject[stat.ST_MTIME]).split()  # e.g [Mon, Jul, 8, 01:16:44, 2019]
            modified_day = "{:02d}".format(int(modified_time[2]))
            modified_month = month_dict.get(str(modified_time[1]))
            modified_year = str(modified_time[-1])
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


if __name__ == "__main__":
    main()

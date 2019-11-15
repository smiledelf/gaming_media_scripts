import os
import stat
import time


def main():
    """
    This program loops through the folder it's placed in and looks for .png files that start with "Screenshot", then
    renames them according to day of creation without duplicates.
    """
    user_proceed()

    # Set up dictionary for month conversion (e.g Jun -> 06)
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
        if file.startswith("Screenshot") and file.lower().endswith(".png"):
            # If a screenshot is found, get its creation metadata
            filepath = os.path.join(os.curdir, file)
            filestatobject = os.stat(filepath)

            # Get file creation time
            creation_time = time.ctime(filestatobject[stat.ST_CTIME]).split()  # e.g [Mon, Jul, 8, 01:16:44, 2019]
            creation_day = "{:02d}".format(int(creation_time[2]))
            creation_month = month_dict.get(str(creation_time[1]))
            creation_year = str(creation_time[-1])
            duplicate_index = 1

            # Propose name with no duplicates
            # e.g 2019_06_26_1
            proposed_filename = creation_year + '_' + creation_month + '_' + creation_day + '_' + \
                str(duplicate_index) + '.png'

            duplicate_exist = os.path.isfile(proposed_filename)

            while duplicate_exist:
                duplicate_index += 1
                proposed_filename = creation_year + '_' + creation_month + '_' + creation_day + '_' + \
                    str(duplicate_index) + '.png'

                duplicate_exist = os.path.isfile(proposed_filename)

            try:
                os.rename(filepath, proposed_filename)
            except FileExistsError:
                print("ERROR: Cannot rename", filepath, "to", proposed_filename + "! File already exists.")


def user_proceed():
    """
    Simple prompt asking user if they want to continue with script.
    """
    print("-----------------------!! WARNING !!---------------------------")
    print("This script will rename any files that start with 'Screenshot'!")
    print("There is no undo function available.")
    print("-----------------------!! WARNING !!---------------------------")
    print("Are you sure you want to proceed? Type y/n below:")

    usr = str(input()).lower()

    if usr == 'y' or usr == 'yes':
        print("--------------------\nBeginning script...\n--------------------")
    elif usr == 'n' or usr == 'no' or usr == 'nah':
        pause = input("Press ENTER to exit...")
        exit()
    else:
        print("Please enter a valid response next time! ")
        pause = input("Press ENTER to exit...")
        exit()


if __name__ == "__main__":
    main()

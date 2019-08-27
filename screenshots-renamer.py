import os
import stat
import time


def main():
    """
    This program loops through the folder it's placed in and looks for .png files that start with "Screenshot", then
    renames them according to day of creation without duplicates.
    """
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
            creation_month = str(creation_time[1])
            creation_year = str(creation_time[-1])
            duplicate_index = 1

            # Propose name with no duplicates
            # e.g 26Aug2019_1
            proposed_filename = creation_day + creation_month + creation_year + '_' + str(duplicate_index) + '.png'
            duplicate_exist = os.path.isfile(proposed_filename)

            while duplicate_exist:
                print(proposed_filename, duplicate_exist)
                duplicate_index += 1
                proposed_filename = creation_day + creation_month + creation_year + '_' + str(duplicate_index) + '.png'

                duplicate_exist = os.path.isfile(proposed_filename)

            try:
                os.rename(filepath, proposed_filename)
            except FileExistsError:
                print("ERROR: Cannot rename", filepath, "to", proposed_filename + "! File already exists.")


if __name__ == "__main__":
    main()



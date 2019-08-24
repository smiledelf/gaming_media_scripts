import os
import stat
import time


def main():
    # Get current directory, then loop through its files to find which ones are screenshots
    current_folder = os.curdir

    for file in os.listdir(current_folder):
        if file.startswith("Screenshot") and file.lower().endswith(".png"):
            # If a screenshot is found, get its creation metadata
            filepath = os.path.join(os.curdir, file)
            filestatobject = os.stat(filepath)

            # Create list containing information about file creation time
            creation_time = time.ctime(filestatobject[stat.ST_CTIME]).split()  # e.g [Mon, Jul, 8, 01:16:44, 2019]

            # Put into readable format, then rename file accordingly
            # e.g 08Jul2019_1
            creation_day = "{:02d}".format(int(creation_time[2]))
            creation_month = str(creation_time[1])
            creation_year = str(creation_time[-1])

            proposed_name = creation_day + creation_month + creation_year + '.png'  # Readable format
            correct_name = duplicate_resolution(proposed_name, 0)   # Readable format AND no duplicates

            os.rename(filepath, correct_name)


def duplicate_resolution(filename, increment):
    """
    This function determines whether a file already exists with the proposed name change.
    If one does, the function determines a unique name for it.

    :param filename: current proposed filename
    :param increment: current index of duplicate (i.e how many duplicates there exists)
    :return: new_filename: filename to be changed
    """

    duplicate_exists = os.path.isfile(os.curdir + filename)
    print(duplicate_exists)

    if increment == 0 and not duplicate_exists:
        print("No dupes exists, returning now")
        print(filename, increment)
        return filename
    else:
        print("Dupe found!")
        next_increment = increment + 1
        new_filename = filename[:-4] + "_" + str(next_increment) + filename[-4:]

        print(new_filename, next_increment)

        duplicate_resolution(new_filename, next_increment)


if __name__ == "__main__":
    main()



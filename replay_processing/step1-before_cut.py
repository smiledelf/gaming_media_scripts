# global imports
from os import path
from os import chdir
from os import listdir
from os import rename
from send2trash import send2trash

"""
Run this BEFORE using LosslessCut. (this has been pre-set for that)
Options refer to the different ways of preprocessing the filenames.
"""

def main():
    # TODO: Remove the useless options (e.g opt2 is a little simple in the head)
    # setting up
    current_directory = path.dirname(path.realpath(__file__))
    chdir(current_directory)
    print("Current script directory: " + current_directory)
    input("--- !!! --- WARNING: Read code first! It's very simple. --- !!! ---\nPress ENTER to continue...")
    # strip_string = input("Enter start of filename (to be stripped): ")
    strip_string = "Replay_"
    extension_string = ".mp4"
    option = 7

    try:

        if option == 0:
            print("No option selected. Please change it in code.")

        elif option == 1:
            # Option 1: Strip a specified substring from the start of filename:
            opn1(current_directory, strip_string)

        elif option == 2:
            # Option 2: Index-based stripping from name - great for renaming
            opn2(current_directory, strip_string)

        elif option == 3:
            # Option 3: Strip and replace by a key phrase
            opn3(current_directory)

        elif option == 4:
            # Option 4: Use index to keep start of filename - great for after LosslessCut
            opn4(current_directory, extension_string)

        elif option == 5:
            # Option 5: AMD Radeon - Remove "replay" nonsense from Radeon Replay filenames
            opn5(current_directory, extension_string)

        elif option == 6:
            # Option 6: Rename the trimmed file after processing in LosslessCut
            # This is the most complex option
            # Every time it runs, it will try to move original and byproduct file into the bin
            # Every time it runs, it will try to rename the trimmed file
            opn6(current_directory, extension_string)

        elif option == 7:
            # Option 7: GeForce Experience - Remove "DVR" and game name, only keep datetime in the name
            opn7(current_directory, extension_string)
    
    except Exception as e:
        print("ERROR: Something went wrong. Error message below...\n\n" + str(e))
        input("\nPress ENTER to continue...")
        

def opn1(current_directory, strip_string):
    for file in listdir(current_directory):
        if file.startswith(strip_string):
            new_name = file.strip(strip_string)
            print(file, "-->>", new_name)
            rename(file, new_name)

def opn2(current_directory, strip_string):
    for file in listdir(current_directory):
        if file.startswith(strip_string):
            new_name = file[:6] + " -" + file[6:]
            print(file, "-->>", new_name)
            rename(file, new_name)

def opn3(current_directory):
    strip_string = "22 07 2020-"
    replace_string = "raw1"
    for file in listdir(current_directory):
        if file.startswith(strip_string):
            new_name = replace_string + "_" + file[len(strip_string):]
            print(file, "-->>", new_name)
            rename(file, new_name)

def opn4(current_directory, extension_string):
    for file in listdir(current_directory):
        if file.endswith(extension_string):
            new_name = file[:16] + extension_string  # or file[-4:] ?
            print(file, "-->>", new_name)
            rename(file, new_name)

def opn5(current_directory, extension_string):
    changes = []
    for file in listdir(current_directory):
        if file.endswith(extension_string) and "replay" in file:
            new_name = file[-20:]  # YYYY.MM.DD-HH.MM.mp4
            change = str(file) + " -->> " + str(new_name)  # to be renamed
            print(change)
            changes.append(change)
            rename(file, new_name)
    if len(changes) > 0:
        f = open("changes.txt", "w")
        for change in changes:
            f.write("%s\n" % change)
        f.close()

def opn6(current_directory, extension_string):
    while True:
        for file in listdir(current_directory):
            # looking for a chonky filename
            # e.g 2022.09.22-12.42-00.01.38.282-00.02.00.016.mp4
            if file.endswith(extension_string) and len(file) == 46:
                print("\nFound a recently-trimmed file!\n" + file)
                date = file[:16]

                # trash original & byproduct files
                try:
                    original = date + extension_string
                    byproduct_dummy_mkv = date + "-html5ified-dummy.mkv"
                    byproduct_csv = date + "-llc-edl.csv"
                    send2trash([original, byproduct_dummy_mkv, byproduct_csv])   
                    print("Deleted", original)
                    print("Deleted", byproduct_dummy_mkv)
                    print("Deleted", byproduct_csv)    
                except Exception as e:
                    print("\nWHOOPSIE: We ran into an error!")
                    print("Most likely errors:\n- Can't find the byproduct files to move to the Recycling Bin (safe to ignore)\n- Original clip is open in another program (try closing VLC, etc.)\n")
                
                # rename trimmed file
                valid_name = False
                while not valid_name:
                    description = str(input(">> Write a description for this clip: "))
                    new_name = date + " " + description + extension_string
                    try:
                        rename(file, new_name)
                        print("Renamed", file, "-->>", new_name)
                        valid_name = True
                    except Exception as e:
                        print("\nWHOOPSIE: We ran into an error!")
                        print("Most likely errors:\n- Filename contains invalid characters (\\ / : * ? \" < > |\n- File is open in another program (try closing VLC, etc.)\nTry again!\n")

        input("Folder scan complete. Press ENTER to re-scan...")

def opn7(current_directory, extension_string):
    # original: "Desktop 2022.12.27 - 22.49.58.05.DVR.mp4" 
    # renamed: "2022.12.27-22.49.mp4"
    changes = []
    for file in listdir(current_directory):
        if file.endswith(extension_string) and "DVR" in file:
            # gather pieces
            ext = file[-4:]
            mm = file[-16:-14] 
            hh = file[-19:-17]
            date = file[-32:-22]
            # combine into new name
            new_name = date + "-" + hh + "." + mm + ext  # YYYY.MM.DD-HH.MM.mp4
            # print, log, and rename
            change = str(file) + " -->> " + str(new_name)  # to be renamed
            print(change)
            changes.append(change)
            rename(file, new_name)
    if len(changes) > 0:
        f = open("changes.txt", "w")
        for change in changes:
            f.write("%s\n" % change)
        f.close()

if __name__ == "__main__":
    main()

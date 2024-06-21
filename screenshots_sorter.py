import os
import steamfront
import logging

# TODO: this class? do i even need tbh?
class ScreenshotSorter():

    client = steamfront.Client()
    accepted_extensions = ('.png', '.jpg', '.jpg')


    def __init__(self, root_dir:str) -> None:
        
        # initialise instance variables
        self.root_dir = root_dir
        self.cache = dict()  # { appid : game object }
        
        # set up logging
        logging.basicConfig(filename='sorting.log', encoding='utf-8', level=logging.DEBUG)


    def sort_screenshots(self, directory:str=None) -> None:

        logging.info("Steam interface loaded, begin scanning directory")
        if directory is None:
            directory = self.root_dir  # this lets us call sort_screenshots() without specifying path if it has been instantiated

        for file in os.listdir(directory):
            if file.endswith(ScreenshotSorter.accepted_extensions):
                logging.info(f"Detected screenshot {file}")

                # get the game of the screenshot
                screenshot_appid = file.split("_")[0]  # appid
                game_name = ""
                if screenshot_appid in self.cache:
                    game_name = self.cache[screenshot_appid]
                    logging.info(f"Game ({game_name}) previously detected, no need to call API again to retrieve name")
                else:
                    # retrieve game object, get the game name, and store to dict
                    game_name = client.getApp(appid=screenshot_appid).name
                    self.cache[screenshot_appid] = game_name
                    logging.info(f"New game detected, API called to get the name of the game ({game_name})")

                
                # validate game name for Windows folder name (Windows)
                invalid_mapping = [(_, " -") for _ in ['<','>',':','"','/','\\','|','?','*',]]
                folder_name = game_name
                for v, k in invalid_mapping:
                    folder_name = folder_name.replace(v, k)
                logging.info(f"Finished validating game name for Windows folder names")


                # create game folder if it doesn't exist
                if not os.path.isdir(folder_name):
                    logging.error(f"Folder {folder_name} could not be found")
                    try:
                        os.mkdir(folder_name)
                        logging.info(f"Created folder {folder_name}")
                    except Exception as e:
                        logging.error(f"Failed to create folder {folder_name}. Exception: {e}")
                
                # move screenshot to its game folder
                file_moved = f"./{folder_name}/{file}"
                try:
                    os.rename(file, file_moved)
                    logging.info(f"Moved file from {file} to {file_moved}")
                except Exception as e:
                    logging.error(f"Failed to moved file from {file} to {file_moved}. Exception: {e}")


if __name__ == "__main__":

    logging.basicConfig(filename='sorting.log', encoding='utf-8', level=logging.DEBUG)
    logging.info("Logging initialised, starting script now.")

    script_path = os.path.realpath(__file__)
    os.chdir(script_path)
    logging.debug(f"Set current working directory to {script_path}")

    client = steamfront.Client()
    logging.debug("Steam API loaded, beginning renaming function.")
    sorter = ScreenshotSorter(script_path)
    sorter.sort_screenshots()
    logging.info("Main module is finished, closing script")
    print("Script is done!")
         


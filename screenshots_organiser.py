import os
import steamfront
from loguru import logger


class ScreenshotOrganiser():

    client = steamfront.Client()
    accepted_extensions = ('.png', '.jpg', '.jpg')


    def __init__(self, root_dir:str) -> None:
        """Instantiate screenshot organiser based on directory given.
        
        :param root_dir: directory to scan
        """
        
        logger.debug(f"Instantiated {self.__class__}")

        self.root_dir = root_dir
        self.cache = dict()  # { appid : game object }
    

    def organise_screenshots(self, directory:str=None) -> None:
        """For a given folder, move loose screenshots into their respective game folders.

        :param directory: directory to organise, defaults to None
        """

        logger.info("Beginning screenshots organising process...")

        if directory is None:
            directory = self.root_dir  # this lets us call the method without specifying path if it has been instantiated

        for file in os.listdir(directory):
            if file.endswith(ScreenshotOrganiser.accepted_extensions):
                logger.debug(f"Detected screenshot {file}")

                # get the game of the screenshot
                screenshot_appid = file.split("_")[0]  # appid
                game_name = ""
                if screenshot_appid in self.cache:
                    game_name = self.cache[screenshot_appid]
                    logger.debug(f"Game ({game_name}) previously detected, no need to call API again to retrieve name")
                else:
                    # retrieve game object, get the game name, and store to dict
                    game_name = client.getApp(appid=screenshot_appid).name
                    self.cache[screenshot_appid] = game_name
                    logger.debug(f"New game detected, API called to get the name of the game ({game_name})")

                # validate game name for Windows folder name (Windows)
                invalid_mapping = [(_, " -") for _ in ['<','>',':','"','/','\\','|','?','*',]]
                folder_name = game_name
                for v, k in invalid_mapping:
                    folder_name = folder_name.replace(v, k)
                logger.debug(f"Finished validating game name for Windows folder names")

                # create game folder if it doesn't exist
                if not os.path.isdir(folder_name):
                    logger.error(f"Folder {folder_name} could not be found")
                    try:
                        os.mkdir(folder_name)
                        logger.debug(f"Created folder {folder_name}")
                    except Exception as e:
                        logger.error(f"Failed to create folder {folder_name}. Exception: {e}")
                
                # move screenshot to its game folder
                file_moved = f"./{folder_name}/{file}"
                try:
                    os.rename(file, file_moved)
                    logger.debug(f"Moved file from {file} to {file_moved}")
                except Exception as e:
                    logger.error(f"Failed to moved file from {file} to {file_moved}. Exception: {e}")

        logger.info("Finished screenshots organising")


if __name__ == "__main__":

    log_path = "screenshots_organiser.log"
    logger.add(sink=log_path)
    
    logger.info("Main function starting.")
    script_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(script_path)
    logger.debug(f"Set current working directory to {script_path}")

    client = steamfront.Client()
    logger.debug("Initialised steamfront to query Steam API")

    organiser = ScreenshotOrganiser(script_path)
    organiser.organise_screenshots()
    
    logger.info("Main function finished, closing script")

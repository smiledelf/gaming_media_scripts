import os
import steamfront
import logging

# TODO: this class? do i even need tbh?
class ScreenshotSorter():

    def __init__(self):
        pass


if __name__ == "__main__":

    print("Starting program...")
 
    logging.basicConfig(filename='script.log', encoding='utf-8', level=logging.DEBUG)
    logging.info('Starting script')

    client = steamfront.Client()
    cache = dict()  # { appid : game object }
    accepted_extensions = ('.png', '.jpg', '.jpg')

    logging.info("Steam interface loaded, begin scanning directory")

    for file in os.listdir():

        if file.endswith(accepted_extensions):

            logging.info(f"Detected screenshot {file}")

            # get the game of the screenshot
            screenshot_appid = file.split("_")[0]  # appid
            game_name = ""

            if screenshot_appid in cache:
                game_name = cache[screenshot_appid]
                logging.info(f"Game ({game_name}) previously detected, no need to call API again to retrieve name")
            else:
                # retrieve game object, get the game name, and store to dict
                game_name = client.getApp(appid=screenshot_appid).name
                cache[screenshot_appid] = game_name
                logging.info(f"New game detected, API called to get the name of the game ({game_name})")

            
            # validate game name for Windows folder name (Windows)
            invalid_mapping = [(v, " -") for v in ['<','>',':','"','/','\\','|','?','*',]]
            folder_name = game_name
            for v, k in invalid_mapping:
                folder_name = folder_name.replace(v, k)
            logging.info(f"Finished validating game name for Windows folder names")


            # create game folder if it doesn't exist
            if not os.path.isdir(folder_name):
                logging.error(f"Folder {folder_name} could not be found")
                try:
                    os.mkdir(folder_name)
                    logging.inf(f"Created folder {folder_name}")
                except Exception as e:
                    logging.error(f"Failed to create folder {folder_name}. Exception: {e}")
            
            # move screenshot to its game folder
            file_moved = f"./{folder_name}/{file}"
            try:
                os.rename(file, file_moved)
                logging.info(f"Moved file from {file} to {file_moved}")
            except Exception as e:
                logging.error(f"Failed to moved file from {file} to {file_moved}. Exception: {e}")

    logging.info("Main module is finished, closing script")
    print("Script is done!")
         


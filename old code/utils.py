import os
import pickle
import re
import json

## Pickle code
def writePickle(file, data):
    try:
        with open(file, "wb") as f:
            pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as err:
        print("Error during pickling (writing).", err)

def loadPickle(file):
    try:
        with open(file, "rb") as f:
            return pickle.load(f)
    except Exception as err:
        print("Error during pickling (loading).", err)
        """
        Errors:
        "Ran out of input" - pkl file is likely empty, check if 'wb' or 'rb' is used.
        """
##

def timeInSeconds(t):
    hrs = int(t / 3600)
    t = t % 3600 
    mins = int(t / 60)
    t = t % 60
    secs = t
    if hrs != 0:
        return "{} hrs, {} mins, {:.03f} s".format(hrs, mins, secs)
    elif mins != 0:
        return "{} mins, {:.03f} s".format(mins, secs)
    else:
        return "{:.03f} s".format(secs)

def dumpJson(data):
    return json.dumps(data, indent=4, sort_keys=True)

def createAllFolders(root, folderpath):
    """
    By the way the variable naming for the function is literally inverted.
    Because I'm an idiot.
    """

    if "\\" in folderpath:
        only_folders = re.search(r".*(?=\\)", folderpath).group()

        if not os.path.exists(os.path.join(root,only_folders)):
            if "\\" not in only_folders:
                current_folder = os.path.join(root,only_folders)
                if not os.path.exists(current_folder):
                    os.mkdir(current_folder)

            else:
                all_folders = re.findall(r'^.*?(?=\\)|(?<=\\).*?(?=\\)|(?<=\\).+$',only_folders)
                current_folder = root

                for folder in all_folders:
                    current_folder = os.path.join(current_folder,folder)
                    if not os.path.exists(current_folder):
                        #print("CREATING "+current_folder)
                        os.mkdir(current_folder)
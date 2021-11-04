import os
import re
import shutil
import time
import socket
from rich import style

from rich.console import Console

import tqdm

from utils import * 
from write_config import viewConfigs, runThis

"""
Notes

socket.gethostname() 
Two options
ZEEE... -> PEG
or SANPEE... -> UC

For PEG
Primarily it's from 

"""

## SETUP VARS !! 
debug = False
# Debug means disabling all OS operations: file and folder copying, history .pkl file creation

## Stuff
def loadConfig():
    global config
    config = loadPickle(r'config.pkl') 

def loadPathPresets(host = "peg", n=0):
    # Defaults are peg and preset 0.
    # LAZY TO WRITE ERROR CODE.

    src_n = config["path presets"][host][n][1]
    dst_n = config["path presets"][host][n][2]

    src_path = config["paths"][host][src_n]
    dst_path = config["paths"][host][dst_n]

    return src_path, dst_path

def createBaseRegexes():
    global ignored_folders_regex, ignored_files_regex
    ignored_folders_regex = re.compile(config["ignored folders"])
    ignored_files_regex = re.compile(config["ignored files"])

    #ignored_folders_regex = re.compile(r'|'.join('$'+str(a) for a in config["ignored folders"]))
    #ignored_files_regex = re.compile(r'|'.join('$'+str(a) for a in config["ignored files"]))

## Real code

def consoleInput():
    #host names and stuff
    hostname = socket.gethostname()
    host = ""
    for options in config["hostnames"]:
        if re.search(options[0], hostname) != None:
            host = options[1]
            break

    # No host auto-identified
    if host == "":
        print("No host has been autoidentified.")
        while True:
            h = input("Please manually enter the host (peg/uc): ")
            if h.lower() == "peg":
                host = "peg"
                break
            elif h.lower() == "uc":
                host = "uc"
                break
            else:
                "Please try again."
    print("Host PC has been identified as '{}'.".format(host))
    
    ## showing the options for presets
    presetText = """"""
    for i, preset in enumerate(config["path presets"][host]):
        presetText += """Preset {} | {}
Source: {},
Destination: {}

""".format(
    i + 1, preset[0],
    config["paths"][host][preset[1]],
    config["paths"][host][preset[2]]
    )
    print(presetText)

    max_n = len(config["path presets"][host])
    # print(max_n)
    while True:
        try:
            n = int(input("Please enter the preset: ")) - 1
            if 0 <= n < max_n:
                break
            print("Invalid preset.")
        except Exception as e:
            print("Invalid preset.", e)

    return host, n

def checkDir(folder_path):
    # NO longer a "check" function lmao.
    # The darker blue syntax highlighting is nice, I'll just keep that. :-P

    ROOTS = []
    FILES = {}
    for root, dirs, files in os.walk(folder_path):
        root_relative = root.replace(folder_path,"")[1:]
        if ignored_folders_regex.search(root_relative) != None:
            # Ignoring ignored folders
            continue
        ROOTS.append(root_relative)
        # maybe do a ROOT CHECK FIRST?

        for f in files:
            if ignored_files_regex.search(f) != None:
                # ignoring ignored files
                continue
            filepath = os.path.join(root, f)
            FILES[filepath.replace(folder_path,"")[1:]] = (os.path.getmtime(filepath), os.stat(filepath).st_size)
            # for the file tuple: (time of creation, size in bytes)

    return ROOTS, FILES

def main():
    ## For Rich
    global console
    console = Console()

    # Debug warning
    if debug:
        console.print("DEBUG IS ENABLED.", style="bold yellow")

    ## init, in case
    global workingDir
    workingDir = os.getcwd()
    ##
    # loadConfig -> Global variable `config`
    loadConfig()
    createBaseRegexes()

    if debug:
        ## Debug Overrides (TODO) - Just to note, it's here btw.
        src_path, dst_path = loadPathPresets(n=1) 
        # n=1 points to the debug directories
        
    elif not debug:
        host, n = consoleInput()
        src_path, dst_path = loadPathPresets(host=host, n=n) 

    ## Start timing.
    global start_time
    start_time = time.time()

    ## TIME TO OS.WALK
    # This is for finding which folders (roots) and
    # files to copy or remove.
    src_roots, src_files = checkDir(src_path)

    ## checks for -icfilehistory.pkl in dst (./)
    dst_roots, dst_files = checkDir(dst_path)
    if os.path.exists(os.path.join(dst_path, config["history filename"])):
        del dst_files
        dst_files = loadPickle(os.path.join(dst_path, config["history filename"]))

    roots_to_remove = []
    roots_to_add = []
    files_to_copy, files_to_remove = {}, []

    # folders to add to dst
    for src_root in src_roots:
        if src_root not in dst_roots:
            roots_to_add.append(src_root)

    # folders to remove from dst
    for dst_root in dst_roots:
        if dst_root not in src_roots:
            roots_to_remove.append(dst_root)

    # Files to copy/overwrite from src to dst.
    for src_file in list(src_files):
        if src_file in list(dst_files):
            if src_files[src_file][0] == dst_files[src_file][0]:
                continue
            else:
                files_to_copy[src_file] = byteConverter(src_files[src_file][1])
        else:
            files_to_copy[src_file] = byteConverter(src_files[src_file][1])

    # Files to remove from dst.
    for dst_file in list(dst_files):
        if dst_file not in list(src_files):
            files_to_remove.append(dst_file)

    # THis might be relegated to ultra-verbose.
    ## A Bunch of printing code
    # print("REMOVE FOLDERS", roots_to_remove)
    # print("\n")
    # print("ADD FOLDERS", dumpJson(roots_to_add))
    # print("\n")
    # print("COPY FILES", dumpJson(files_to_copy))
    # print("\n")
    # print("REMOVE FILES", dumpJson(files_to_remove))

    # print(len(files_to_copy))
    # print(files_to_copy[980])
    # print(files_to_copy[1562])
    # print(files_to_copy[2766])

    #### SYNCING TIME !
    for root in roots_to_remove:
        try:
            # Remove folders
            if not debug:
                os.rmdir(os.path.join(dst_path, root))

            console.print("Removed folder: [gray]{}".format(root))

        except Exception as err:
            console.print(err, style="bold red")
            input("Press enter to continue.")

    for root in roots_to_add:
        try:
            # Add folders
            if not debug:
                createAllFolders(dst_path, root + "\\")

            console.print("Created folder: [gray]{}".format(root))

        except Exception as err:
            console.print(err, style="bold red")
            input("Press enter to continue.")

    for file in list(files_to_copy):
        try:
            # Remove, then copies file.
            if not debug:
                full_dst_path, full_src_path = os.path.join(dst_path, file), os.path.join(src_path, file)
                if os.path.exists(full_dst_path):
                    os.remove(full_dst_path)
                shutil.copy(full_src_path, full_dst_path)

            console.print("Copied file: [gray]{}   [{}]".format(file, files_to_copy[file]))

        except Exception as err:
            console.print(err, style="bold red")
            input("Press enter to continue.")

    for file in files_to_remove:
        try:
            # Removes files.
            if not debug:
                full_dst_path = os.path.join(dst_path, file) 
                os.remove(full_dst_path)

            console.print("Removed file: [gray]{}".format(file))

        except Exception as err:
            console.print(err, style="bold red")
            input("Press enter to continue.")

    ## Creating -icfilehistory.pkl in dst (./)
    # I think just dumping the src_files dict is fine, 
    # seeing as it's supposed to be dst_files
    if not debug:
        writePickle(os.path.join(dst_path, config["history filename"]), data=src_files)

    ### End of script
    console.print("\nTime elapsed: {}".format(timeInSeconds(time.time() - start_time)))

    if not debug:
        input("Syncing complete. Press enter to close.")

if __name__ == "__main__":
    runThis() # Writes updated configs.
    main()

    
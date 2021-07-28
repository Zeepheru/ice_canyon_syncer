import os
import re
import shutil
import time

### path vars
global src_path, dst_path, perfect_sync_folders, add_sync_folders, start_time
src_path = r'C:\Users\chang\Documents\Ice Canyon'
dst_path = r'F:\Ice Canyon (Thumbdrive Version)'
start_time = time.time()

#FILE SIZE CODE DOESNT SEEM TO WORK AT THE MOMENT

folder_options = [
    {
    "name":"IC Default (Peg) -> IC Thumb",
    "src":r'C:\Users\chang\Documents\Ice Canyon',
    "dst":r'F:\Ice Canyon (Thumbdrive Version)'
    },
    {
    "name":"IC Default (Peg) -> IC Backup (Peg)",
    "src":r'C:\Users\chang\Documents\Ice Canyon',
    "dst":r'D:\Brownie\My Little Pony\Ice Canyon Backup'
    },
    {
    "name":"IC Thumb -> IC Backup (Uc-Narwhal)",
    "src":r'G:\Ice Canyon (Thumbdrive Version)',
    "dst":r'I:\Backup\Pony\MLP\Ice Canyon Backup'
    },
    {
    "name":"IC Backup (Uc-Narwhal) -> IC Backup2 (Uc-Brownie)",
    "src":r'I:\Backup\Pony\MLP\Ice Canyon Backup',
    "dst":r'P:\MLP\Ice Canyon Backup'
    },
]

def return_time_from_seconds(t):
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

perfect_sync_folders = [
    "root",
    "Chocolate",
    "Circles",
    "crits",
    "Griffons",
    "Reindeer",
    "[Export]",
    "[Works]",
    "[References]"
    ]
add_sync_folders = [
    "Revisit",
    "Practice",
    "Milk"
    ] 
#Probably need the in progress folders as well.

def main():
    global src_path, dst_path, perfect_sync_folders, add_sync_folders

    def btf(list_folders):
        new_list = []
        for a in list_folders:
            new_list.append("\\{}\\".format(a)[1:-1])
        return new_list

    def createallfolders(root,filepath):
        if "\\" in filepath:
            only_folders = re.search(r".*(?=\\)", filepath).group()

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

    def perfect_sync(src_file_path, dst_file_path):
        #Needs a delete in dst if not in src function as well.

        if os.path.exists(dst_file_path):
            if not os.path.exists(src_file_path):
                #untested lol
                print("Removing [{}] from dst.".format(relative_path))
                os.remove(dst_file_path)

            #print(f, str(os.stat(src_file_path).st_size), str(os.stat(dst_file_path).st_size))
            elif os.stat(src_file_path).st_size != os.stat(dst_file_path).st_size:
                print("Copying [{}] (Different File Sizes)".format(relative_path))
                createallfolders(dst_path, relative_path)
                shutil.copy(src_file_path, dst_file_path)
                #os.remove(src_file_path) #WHY THE F IS THIS HERE?????
            else:
                pass
        else:
            print("Copying [{}]".format(relative_path))
            createallfolders(dst_path, relative_path)
            shutil.copy(src_file_path, dst_file_path)

    #creating the 
    options_text = ""
    for i, option in enumerate(folder_options):
        i += 1
        options_text += "   {} - {}\n".format(i, option["name"])
        ##

    input1  = input("""Ice Canyon Syncer script.
Main Directory Options:
{}
If a manual entry is required, enter (n):

[-d] to remove all files from dst.
""".format(
    options_text
    ))
    default_dir_options = False
    try:
        int(input1[:1])
        if default_dir_options <= + len(folder_options):
            default_dir_options = True
        else:
            pass
    except:
        pass
    
    #actual dir shutfff
    if default_dir_options:
        if "-d" in input1:
            remove_dst = True
        else:
            remove_dst = False

        input1 = int(input1[:1])

        src_path = folder_options[input1-1]["src"]
        dst_path = folder_options[input1-1]["dst"]

        ## Removing files from dst
        if remove_dst:
            print("Removing files from [{}].".format(dst_path))
            for root, dirs, files in os.walk(dst_path):
                for f in files:
                    try:
                        os.remove(os.path.join(root, f))
                    except:
                        pass
    else:
        src, dst  = False, False
        while src == False:
            src_path = input("Change source path: ")
        
            if not os.path.exists(src_path):
                print("Source path is not valid. (Does not exist)")
            else:
                src = True

        while dst == False:
            dst_path = input("Change destination path: ")
            
            try:
                if not os.path.exists(dst_path):
                    os.mkdir(dst_path)
                    print('Destination directory [{}] created'.format(dst_path))
                dst = True
            except:
                print("Destination path is not valid.")

    if not os.path.exists(dst_path):
        os.mkdir(dst_path)
        print('Destination directory [{}] created.'.format(dst_path))

    ##Actual copier code
    print("""Syncing Ice Canyon Files...
    From: [{}]
    To: [{}]
    
Folders to be synced perfectly (if file sizes are different): {}
Folders to be synced with addition of files to dst: {}
""".format(
    src_path, dst_path,
    str(btf(perfect_sync_folders))[1:-1].replace("'",''), str(btf(add_sync_folders))[1:-1].replace("'",'')
    ))


    missing_folders = []
    src_root_dir_list = os.listdir(src_path)
    for folder in perfect_sync_folders + add_sync_folders:
        
        if folder not in src_root_dir_list and folder != 'root':
            missing_folders.append(folder)
        
    if missing_folders != []:
        print("Folders: "+ str(btf(missing_folders))[1:-1].replace("'",'') + " are not found in source directory.\n")


    ignored_folders = []
    for folder in src_root_dir_list:
        folder_actual = re.search(r'\.[a-zA-Z]{2,4}',folder)
        if folder_actual == None:
            folder_actual = folder
            if folder_actual not in perfect_sync_folders + add_sync_folders:
                ignored_folders.append(folder_actual)
        
    if ignored_folders != []:
        print("Folders: "+ str(btf(ignored_folders))[1:-1].replace("'",'') + " will not be synced.\n")

    for root, dirs, files in os.walk(src_path):
        for f in files:
            if f != "Thumbs.db":
                src_file_path = os.path.join(root,f)
                relative_path = src_file_path.replace(src_path,"")[1:]
                dst_file_path = os.path.join(dst_path,relative_path)

                file_folder = re.search(r'.*?(?=\\)',relative_path)
                if file_folder != None:
                    
                    file_folder = file_folder.group()
                    #print(f, file_folder)

                    if file_folder in perfect_sync_folders:
                        perfect_sync(src_file_path, dst_file_path)

                    if file_folder in add_sync_folders:
                        if not os.path.exists(dst_file_path):
                            print("Copying [{}]".format(relative_path))

                            createallfolders(dst_path, relative_path)
                            
                            shutil.copy(src_file_path, dst_file_path)

                else:
                    #print(f)
                    if "root" in add_sync_folders:
                        pass #NOT NEEDED, will never need
                    elif "root" in perfect_sync_folders:
                        perfect_sync(src_file_path, dst_file_path)

    #removalcode
    for root, dirs, files in os.walk(dst_path):
        for f in files:
            if f != "Thumbs.db":
                dst_file_path = os.path.join(root,f)
                relative_path = dst_file_path.replace(dst_path,"")[1:]
                src_file_path = os.path.join(src_path,relative_path)

                file_folder = re.search(r'.*?(?=\\)',relative_path)
                if file_folder != None:
                    
                    file_folder = file_folder.group()
                    #print(f, file_folder)

                    if file_folder in perfect_sync_folders:
                        perfect_sync(src_file_path, dst_file_path)

                else:
                    if "root" in perfect_sync_folders:
                        perfect_sync(src_file_path, dst_file_path)
                    

if __name__ == "__main__":
    main()
    print(return_time_from_seconds(time.time() - start_time))
    input("Syncing completed.")
import os
import re
import shutil

### path vars
global src_path, dst_path, perfect_sync_folders, add_sync_folders
src_path = r'C:\Users\chang\Documents\Temp Brownie'
dst_path = r'F:\Temp Brownie'

perfect_sync_folders = ["root","Chocolate","Circles","crits","Griffons","NICE STUFF","Reindeer"]
add_sync_folders = ["HERE ARE SOME FECKING TUTORIALS","IC-","ImR Temp 11","Ref.IC"]

def main():
    global src_path, dst_path, perfect_sync_folders, add_sync_folders

    def btf(list_folders):
        new_list = []
        for a in list_folders:
            new_list.append("\\{}\\".format(a))
        return new_list

    def createallfolders(root,filepath):
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

    input1  = input("""Ice Canyon Syncer script.
For confirmation, the sync source path is {} and the destination path is {}. (y/n)""".format(
    src_path, dst_path
    ))
    if input1 != "y":
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
                    print('Destination directory {} created'.format(dst_path))
                dst = True
            except:
                print("Destination path is not valid.")

    if not os.path.exists(dst_path):
        os.mkdir(dst_path)
        print('Destination directory {} created'.format(dst_path))

    ##Actual copier code
    print("""Syncing Ice Canyon Files...
    
Folders to be synced perfectly (if file sizes are different): {}
Folders to be synced with addition of files to dst: {}
""".format(
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
            src_file_path = os.path.join(root,f)
            relative_path = src_file_path.replace(src_path,"")[1:]
            dst_file_path = os.path.join(dst_path,relative_path)

            file_folder = re.search(r'.*?(?=\\)',relative_path)
            if file_folder != None:
                
                file_folder = file_folder.group()

                if file_folder in perfect_sync_folders:
                    if os.path.exists(dst_file_path):
                        if os.stat(src_file_path).st_size != os.stat(dst_file_path).st_size:
                            os.remove(dst_file_path)
                        else:
                            break
                    else:
                        pass

                    print("Syncing {}".format(relative_path))
                    createallfolders(dst_path, relative_path)
                    shutil.copy(src_file_path, dst_file_path)

                if file_folder in add_sync_folders:
                    if not os.path.exists(dst_file_path):
                        print("Syncing {}".format(relative_path))

                        createallfolders(dst_path, relative_path)
                        
                        shutil.copy(src_file_path, dst_file_path)

            else:
                if "root" in add_sync_folders:
                    pass #NOT NEEDED, will never need
                elif "root" in perfect_sync_folders:
                    if os.path.exists(dst_file_path):
                        if os.stat(src_file_path).st_size != os.stat(dst_file_path).st_size:
                            os.remove(dst_file_path)
                        else:
                            break
                    else:
                        pass

                    print("Syncing {}".format(relative_path))
                    shutil.copy(src_file_path, dst_file_path)
                    

    input("Syncing completed.")


if __name__ == "__main__":
    main()
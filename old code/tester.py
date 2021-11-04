import os

src_file_path = r'I:\Backup\Pony\MLP\Music\Brony Music\Octavia.mp3'
dst_file_path = r'I:\Backup\Pony\MLP\Music\Brony Music\Readme.txt'

print(os.stat(src_file_path).st_size)
print(os.stat(dst_file_path).st_size)
if int(os.stat(src_file_path).st_size) != int(os.stat(dst_file_path).st_size):
    print("Is not the same")
else:
    print("The same for some reason.")
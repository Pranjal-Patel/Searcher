from operator import truediv
import os
from pickletools import optimize
import threading
import pickle

files = {}
# folders = {}
search_path = ""
with open("path.txt", "r") as path_file:
    search_path = path_file.read()

def pr(text):
    print(text)
def extras1(item, file_path):
    th = threading.Thread(target=pr, args=("adding " + item, ))
    # th.daemon = True
    th.start()
    # th.join()
    if item not in files.keys():
        files[item] = file_path
    else:
        index = 1
        while True:
            if item + f"({index})" in files.keys():
                index+=1
            else:
                files[item + f"({index})"] = file_path
                break

def get(path):
    try:
        folders = os.listdir(path)
        for item in folders:
            file_path = os.path.join(path, item)
            if os.path.isfile(file_path):
                th = threading.Thread(target=extras1, args=(item, file_path))
                th.daemon = True
                th.start()
                th.join()
            else:
                # print("\nfolder added " + item, end="")
                # folders[item] = file_path
                th = threading.Thread(target=get, args=(file_path,))
                th.daemon = True
                th.start()
                th.join()
    except PermissionError:
        pass
    except Exception:
        pass

print(f"Searching in \"{search_path}\"")

# start = time.time()
if not os.path.isfile("file_index.pkl"):
    print("File indexing started...")
    get(search_path)
    print("File indexing finished...")

    # File indexing
    f_ = open("file_index.pkl", "wb")
    pickle.dump(files, f_)

    # Folder indexing
    # d_ = open("folder_index.pkl", "wb")
    # pickle.dump(folders, d_)
else:
    option = input("Index file exist do you wanna load ? (type 1 to load and 2 to reload) >")
    if option == " ":
        f_ = open("file_index.pkl", "rb")
        files = pickle.load(f_)
    elif option == '1':
        # File indexing
        f_ = open("file_index.pkl", "rb")
        files = pickle.load(f_)

        # Folder indexing
        # d_ = open("folder_index.pkl", "rb")
        # folders = pickle.load(d_)
    elif option == '2':
        print("File indexing started...")
        get(search_path)
        print("File indexing finished...")

        # File indexing
        f_ = open("file_index.pkl", "wb")
        pickle.dump(files, f_)
    else:
        f_ = open("file_index.pkl", "rb")
        files = pickle.load(f_)

        # # Folder indexing
        # d_ = open("folder_index.pkl", "wb")
        # pickle.dump(folders, d_)
# end = time.time()
# print("Finished in " + str(round(end-start)) + "s")

print("Enter the file you wanna search for, type ~q to quit\n", end="")
while True:
    file = input("filename >")
    if file == " ":
        continue
    if file == "~q":
        break
    try:
        print()
        for key, value in files.items():
            [print(f"{key}: \"{value}\"") if file in key else print("" , end="")]
        print()
    except KeyError:
        print(f"Can't find the file named \"{file}\"")

# print(files)
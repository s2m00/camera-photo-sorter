import os

'''
    For the given path, get the List of all files in the directory tree 
'''


def getPhotoFiles(dirName):
    # print('GetFiles : getListOfFiles : dirName = ', dirName)
    # create a list of file and sub directories
    # names in the given directory
    if not os.path.isdir(dirName):
        return None

    list_of_file = os.listdir(dirName)
    all_files = list()
    # Iterate over all the entries
    for entry in list_of_file:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            all_files = all_files + getPhotoFiles(fullPath)
        else:
            all_files.append(fullPath)

    return photos(all_files)


# return all photo files
def photos(files_list):
    picType = {".jpg", ".png", ".JPG", ".PNG"}

    photo_list = list()
    for file in files_list:
        filePath, fileExeption = os.path.splitext(file)
        if fileExeption in picType:
            photo_list.append(file)

    return photo_list


def get_size(start_path='.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size

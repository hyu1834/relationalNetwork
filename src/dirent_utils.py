## @package dirent_util_module
# Documentation for dirent_util module.
# this modules contains all the functions for any file/directory operation
# More details.
# remove file, create directory, clear directory\n

import sys
import os
import shutil
import io_utils



# Documentation for remove_files
# remove all file in the list
# More details.
# Arguements:\n
# \tf - list of file paths to be remove
def remove_files(f):
    for _file in f:
        try:
            os.remove(_file)

        except KeyboardInterrupt:
            sys.exit(0)
        except SystemExit:
            sys.exit(0)
        except Exception as e:
            io_utils.function_stderr("unable to remove %s due to: %s" % (_file,e.message),"e00000101")

# Documentation for remove_file
# remove single file provided
# More details.
# Arguements:\n
# \tf - single file path
def remove_file(f):
    try:
        os.remove(f)

    except KeyboardInterrupt:
        sys.exit(0)
    except SystemExit:
        sys.exit(0)
    except:
        error("unable to remove %s" % (f),"e00000102")

# Documentation for clear_directory
# remove everything in the directory provided
# More details.
# Arguements:\n
# \tdirectory_name - path of directory
def clear_directory(directory_name):
    try:
        listOfFiles=os.listdir(directory_name)
        for f in listOfFiles:
            if os.path.isdir(directory_name+"/"+f) or os.path.islink(directory_name+"/"+f):
                clear_directory(directory_name+"/"+f)
                os.rmdir(directory_name+"/"+f)
            else:
                os.remove(directory_name+"/"+f)

    except KeyboardInterrupt:
        sys.exit(0)
    except SystemExit:
        sys.exit(0)
    except:
        error("unable to remove %s" % file,"p00000201")

# Documentation for create_directory
# create new directory with the name and path provided
# More details.
# Arguements:\n
# \tdirectory_name - path of directory and name
def create_directory(directory_name):
    try:
        if os.path.exists(directory_name):
        #directory already exist# 
            clear_directory(directory_name)
            return(True)
        elif not os.path.exists(directory_name):
            #if not exist, create one#
            os.makedirs(directory_name)
            return(True)
        else:   #if anything else#
            return(False)

    except KeyboardInterrupt:
        sys.exit(0)
    except SystemExit:
        sys.exit(0)
    except:
        warning("unable to locate/create Directory %s"%directory_name)
        return(False)

def create_new_directory(self,directory_name):
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
    return (directory_name+'/')

# Documentation for list_files_in_directory
# list all files in directory, files only, not including sub-directory\n
# function will return a iteratible
# More details.
# Arguements:\n
# \tdirectory_path - path of directory and name
def list_files_in_directory(directory_path):
    if not os.path.isdir:
        return []

    return [os.path.join(directory_path,_file) for _file in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path,_file))]

# Documentation for list_subdir_in_directory
# list all files in directory, sub-directory only, not including files\n
# function will return a iteratible
# More details.
# Arguements:\n
# \tdirectory_path - path of directory and name
def list_subdir_in_directory(directory_path):
    if not os.path.isdir:
        return []

    return [os.path.join(directory_path,_file) for _file in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path,_file))]

    # for _file in os.path.listdir(directory_name):
    #     full_path = os.path.join(directory_path,_file)
    #     if os.path.isdir(os.path.join(directory_path,_file)):
    #         yield full_path

# Documentation for list_subdir_in_directory
# list all files in directory\n
# function will return a iteratible
# More details.
# Arguements:\n
# \tdirectory_path - path of directory and name
def list_all_in_directory(directory_path):
    if not os.path.isdir:
        return []

    return os.listdir(directory_path)
    # for _file in os.path.listdir(directory_name):
    #     full_path = os.path.join(directory_path,_file)
    #     yield full_path

def get_file_size(path):
    return os.path.getsize(path)

def copy_files(source, destination):
    if type(source) == list:
        for src in source:
            shutil.copy2(src, destination)
    else:
        shutil.copy2(source, destination)

def move_file(source, destination):
    if type(source) == list:
        for src in source:
            shutil.move(src, destination)
    else:
        shutil.move(source, destination)

def is_file_exist(path):
    if os.path.isfile(path):
        return True
    return False

def is_directory_exist(path):
    if os.path.isdir(path):
        return True
    return False

def get_directory_path(path):
    return os.path.dirname(path)

def get_file_basename(path):
    return os.path.basename(path)

def rename_file(source, destination):
    os.rename(source, destination)

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print('usage: python dirent_util.py <option>[option_arguement]')
        sys.exit(0)

    option = '-l'
    option_arguement = None

    for i in range(1,len(sys.argv)):
        if '-' in sys.argv[i][0]:
            option = sys.argv[i]
        else:
            option_arguement = sys.argv[i]

    if option == '-lf' and option_arguement:
        for _file in list_files_in_directory(option_arguement):
            print(_file)
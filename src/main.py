import validation
import ftpserver
from os import listdir
from os.path import isfile, join


#check file names for easy hits

def check_all(downloaded_files):
    for file in downloaded_files:
        return validation.validate_filename(file)

    
#grab files from tmp
def grab_files():
    ftpserver.pullSamples()
    file_list = [f for f in listdir("./tmp") if isfile(join("./tmp", f))]
    return file_list

#main function
def main():
    file_list = grab_files()
    for i in file_list:      
        if (check_all(i)):
            print("file valid")
        else:
            print("file invalid")
from genericpath import exists
import json
import os
from datetime import datetime
from pathlib import Path

cwd = "E:\ScriptTesting"
incNum = "1"
logfile = {}
jsonInfo = {}
run_once = 0
Check = Path(cwd + "/completed")
# JsonLog = open('JsonLog.txt', 'a') Place holder for easy copy paste of opening and writing info to txt file

# JSON PROCESSING
def RenameFiles(path):
    for file in os.listdir(path):
        if file.endswith('.json'):
            # split the filename from extension and store in var
            filename = os.path.splitext(file)
            # open the json file and save into var
            json_file = open(head + "/" + file)
            data = json.load(json_file)
            # pull the timestamp the photo was taken from json file downloaded with pictures, (timestamp is embedded behind two json keys)
            takenTime = data.get('photoTakenTime')
            ts = takenTime.get('timestamp')
            realTime = datetime.utcfromtimestamp(int(ts)).strftime('%m-%d-%Y H%H-M%M-S%S')
            # add file name and real time stamp to dictionary to access later
            jsonInfo[filename[0]] = realTime

# Picture Matching with JSON File then updating Name
        if file.endswith(('.jpg', '.JPG', '.png', '.PNG', '.mov', '.MOV', '.jpeg', '.JPEG'),):
            if file in jsonInfo.keys():
                global incNum
                try:
                    new_name = jsonInfo[file]
                    file_name, file_extension = os.path.splitext(file)
                    new_head = head + "/completed"
                    os.rename(head  + "/" + file,new_head + "/" + new_name + file_extension)
                except:
                    new_name = jsonInfo[file]
                    file_name, file_extension = os.path.splitext(file)
                    new_head = head + "/completed"
                    editedFile = new_head + "/" + str(new_name) + "(" + incNum + ")" + file_extension
                    if editedFile in Check.iterdir():
                        incNum += "1"
                    os.rename(head  + "/" + file, new_head + "/" + str(new_name) + "(" + incNum + ")" + file_extension)
                    incNum += "1"
            else:
                logfile[head + "/" + tail] = " is not in JSON Dict"

# Function for Navigating through directories and sub directories
for path in Path(cwd).rglob('*'):
    if path.is_file():
        # couldn't find a better method for transferring the dir path other than this,
        # which transfers the dir path everytime it finds a file
        head, tail = os.path.split(path)
        #print(head + "\t" + tail)
        RenameFiles(head)

# Code for Logging JsonInfo Dict and logfile (bad file) Dict to .txt file for Error tracking
    if run_once == 0:
        with open('JsonLog.txt', 'a') as Jsondata:
            for k, v in jsonInfo.items():
                Jsondata.write('* %s: %s\n' % (k, v))
        with open('Log.txt', 'a') as Logdata:
            for k, v in logfile.items():
                Logdata.write('* %s: %s\n' % (k, v))
        run_once += 1

#LINUX FILE PATH
# /home/snider/Desktop/testing
#
# Linux only Code for converting .HEIC to .JPG (copied from linux vm)
# Need these packages
#
# from PIL import Image
# import os
# import subprocess
#
# for file in os.listdir(cwd):
#         if file.endswith('.HEIC'):
#                 try:
#                         Chad = Image.open(cwd + "/" + file)
#                         file_name, file_extension = os.path.splitext(file)
#                         Chad.save(cwd + "/" + file_name + '.JPG')
#                 except:
#                         logfile.write(cwd + "/" + file + "\t Invalid File!! \n")
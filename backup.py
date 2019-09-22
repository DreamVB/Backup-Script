# A simple backup script for backing up sets of folders
#
import os
import shutil
import cfgread
import sys
import datetime

def stripPath(lzPath):
    x = str.index(lzPath,":\\")
    if x:
        return lzPath[x+2:]

def fixPath(lzPath):
    if lzPath[len(lzPath) - 1] == "\\":
        return lzPath
    else:
        return lzPath + "\\"

def Backup(Source,Dest):
    file_count = 0
    for root, dir, files in os.walk(Source, topdown=True):
        for file in files:
            file_path = fixPath(root)
            full_file = file_path + file
            back_dir = Dest + stripPath(file_path)
            back_file = back_dir + file
            if not os.path.exists(back_dir):
                # create the backup name folder
                os.makedirs(back_dir)
            shutil.copyfile(full_file,back_file)
            # INC file counter
            file_count += 1
            print("Backing up file: " + file)

    print(str(file_count) + " Files have been copied up.")
    print("")

if len(sys.argv) < 2:
    print("The syntax of the command is incorrect.")
    exit(1)

# Get script file
backup_script = sys.argv[1]

# Get back up script
if not os.path.exists(backup_script):
    print("Backup script was not found.")
    print(backup_script)
    exit(1)

# Load script in config reader
cfgread.loadCfg(backup_script)
backups = int(cfgread.readVal("backups"))

print("Backup created: " + str(datetime.datetime.now()))
print("Please wait backup in process....")
print("")

for x in range(backups):
    copy_from = cfgread.readVal("backup_from" + str(x + 1))
    copy_to = cfgread.readVal("backup_to" + str(x + 1))
    print("Running backup [" + str(x + 1) + "]")
    if os.path.exists(copy_from):
        # Do the backup
        Backup(copy_from,copy_to)

print("")
print(str(x + 1) + " Backups(s) have been created.")

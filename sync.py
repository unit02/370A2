#!/usr/bin/env python3

import sys
import os
import shutil
import json
import time
import hashlib

firstDirectory = sys.argv[1]
secondDirectory = sys.argv[2]


def checkInputDirectories():
    #Neither of the inputs are directories
    if not (os.path.isdir(firstDirectory)) and not ( os.path.isdir(secondDirectory)):
        print("Those aren't directories!")

    #The first directory is real, must create second one
    elif (os.path.isdir(firstDirectory)) and not ( os.path.isdir(secondDirectory)):
        print("The first directory is real, must create second one")

        createNewDirectory(secondDirectory)
        copyFilesInDirectory(firstDirectory,secondDirectory)


    #The second directory is real, must create first one
    elif not (os.path.isdir(firstDirectory)) and ( os.path.isdir(secondDirectory)):
        createNewDirectory(firstDirectory)
        copyFilesInDirectory(secondDirectory,firstDirectory)

    #Otherwise they are both directories yay!


def createNewDirectory(directoryToMake):
    os.makedirs(directoryToMake)

def copyFilesInDirectory(inputDirectory,outputDirectory):
    print("Copying files...")
    fileList = os.listdir(inputDirectory)
    for file in fileList:
        if not file.startswith('.'):
            fullName = os.path.join(inputDirectory, file)
            if (os.path.isfile(fullName)):
                shutil.copy(fullName, outputDirectory)

def compareDirectoryFiles(directoryOne,directoryTwo):
    pass

def encodeFile(fileToEncode):
    h = hashlib.sha256()
    with open(fileToEncode, 'rb') as file:
        buffer = file.read()
        h.update(buffer)
    return h.hexdigest()


def createSyncFile(inputDirectory):
    fileList = os.listdir(inputDirectory)
    with open('.sync', 'w') as outfile:
        for file in fileList:
            if not file.startswith('.'):
                fullName = os.path.join(inputDirectory, file)
                if (os.path.isfile(fullName)):
                    digest = encodeFile(fullName)
                    json.dump({file.title():  [time.strftime("%Y-%m-%d %H:%M:%S %z"), digest] }, outfile,indent=4)

def updateSyncFile(inputDirectory):
    pass

if __name__ == "__main__":
    checkInputDirectories()
    createSyncFile(firstDirectory)
    createSyncFile(secondDirectory)
    updateSyncFile(firstDirectory)


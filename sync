#!/usr/bin/env python3

import sys
import os
import shutil
import json
import time
import hashlib
from collections import defaultdict

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
    jsonDict = {}
    fileList = os.listdir(inputDirectory)
    with open((os.path.join(inputDirectory, '.sync')), 'w') as outfile:
        for file in fileList:
            if not file.startswith('.'):
                fullName = os.path.join(inputDirectory, file)
                if (os.path.isfile(fullName)):
                    digest = encodeFile(fullName)
                    jsonDict[file] = []
                    jsonDict[file].append((time.strftime("%Y-%m-%d %H:%M:%S %z"), digest))
        json.dump(jsonDict, outfile,indent=4)

def updateSyncFile(inputDirectory):
    #load in json file, check if hash is different, check if date different

    with open(os.path.join(inputDirectory, '.sync')) as json_data:
        jsonDict = json.load(json_data)

    newdict = defaultdict(str,jsonDict)

    for file in jsonDict:
        fullName = os.path.join(inputDirectory, file)

        newDigest = encodeFile(fullName)

        if not newDigest == jsonDict[file][0][1]:
            newdict[file].append((time.strftime("%Y-%m-%d %H:%M:%S %z"), newDigest))

    with open((os.path.join(inputDirectory, '.sync')), 'w') as outfile:
        json.dump(newdict, outfile,indent=4)
            #jsonDict[file.title()] = [time.strftime("%Y-%m-%d %H:%M:%S %z"), digest]


def compareFile(dirOneFile,dirTwoFile):
    pass

def updateToLatest(dirOneFile,dirTwoFile):
    pass


if __name__ == "__main__":
    checkInputDirectories()
    #createSyncFile(firstDirectory)
    #createSyncFile(secondDirectory)
    updateSyncFile(secondDirectory)


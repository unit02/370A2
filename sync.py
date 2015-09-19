#!/usr/bin/env python3

import sys
import os
import shutil
import json
import time
import hashlib
from collections import defaultdict
import datetime

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
        if not file.startswith('.') and not file.endswith('~'):
            fullName = os.path.join(inputDirectory, file)
            if (os.path.isfile(fullName)):
                shutil.copy(fullName, outputDirectory)


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
            if not file.startswith('.') and not file.endswith('~') :
                fullName = os.path.join(inputDirectory, file)
                if (os.path.isfile(fullName)):
                    digest = encodeFile(fullName)
                    jsonDict[file] = []
                    jsonDict[file].append((time.strftime("%Y-%m-%d %H:%M:%S %z"), digest))
        json.dump(jsonDict, outfile,indent=4)

def updateSyncFile(inputDirectory):
    #load in json file, check if hash is different, check if date different

    with open(os.path.join(inputDirectory, '.sync')) as jsonData:
        jsonDict = json.load(jsonData)

    newDict = defaultdict(str,jsonDict)

    for file in jsonDict:
        fullName = os.path.join(inputDirectory, file)

        newDigest = encodeFile(fullName)

        if not newDigest == jsonDict[file][0][1]:
            newDict[file].insert(0, (time.strftime("%Y-%m-%d %H:%M:%S %z"), newDigest))

    #add in any files not already in file
    fileList = os.listdir(inputDirectory)
    for file in fileList:
        if not file.startswith('.') and not file.endswith('~') :
            fullName = os.path.join(inputDirectory, file)
            if (os.path.isfile(fullName)):
                digest = encodeFile(fullName)
                if file not in newDict:
                    newDict[file] = []
                    newDict[file].append((time.strftime("%Y-%m-%d %H:%M:%S %z"), digest))

    with open((os.path.join(inputDirectory, '.sync')), 'w') as outfile:
        json.dump(newDict, outfile,indent=4)



def compareDirectories():
    updateSyncFile(firstDirectory)
    updateSyncFile(secondDirectory)

    with open(os.path.join(firstDirectory, '.sync')) as jsonData:
        dirOneJson = json.load(jsonData)

    with open(os.path.join(secondDirectory, '.sync')) as jsonDataTwo:
        dirTwoJson = json.load(jsonDataTwo)

    for file in dirOneJson:
        fullName = os.path.join(firstDirectory, file)
        if file not in dirTwoJson:
            shutil.copy(fullName, secondDirectory)
            updateSyncFile(secondDirectory)
        else:
            fileOne = dirOneJson[file][0]
            fileTwo = dirTwoJson[file][0]
        #file exists in d2, check date, if diff the, then hash. if diff and date
            dirOneDigest = fileOne[1]
            dirTwoDigest = fileTwo[1]
            #Digests are same, date is diff
            if dirOneDigest == dirTwoDigest:

                if fileOne[0] != fileTwo[0]:
                    mostRecentIsOne = getMostRecentDate(fileOne,fileTwo)
                    if(mostRecentIsOne
                        ):
                        addUpdatedDate(secondDirectory, file,dirTwoDigest,fileOne[0])
                    else:
                        addUpdatedDate(firstDirectory, file,dirOneDigest,fileTwo[0])
            else:
                #Files are different, if dates are different get the most recent one and replace the other file
                print("digest diff, if dates are diff get most up to date one")
                mostRecentIsOne = getMostRecentDate(fileOne,fileTwo)
                if(mostRecentIsOne):
                    copyFileInfo(file,secondDirectory,firstDirectory)
                    updateSyncFile(firstDirectory)
                    #the first file is newest, so replace the contents of file two with file one
                else:
                        copyFileInfo(file,firstDirectory,secondDirectory)
                        updateSyncFile(secondDirectory)

                    #diff digest, same date

    for file in dirTwoJson:
        fullName = os.path.join(secondDirectory, file)
        if file not in dirOneJson:
            shutil.copy(fullName, firstDirectory)
            updateSyncFile(firstDirectory)


def copyFileInfo(inputFile,inputDirectory,outputDirectory):
    readFromFile = os.path.join(inputDirectory, inputFile)
    addInfoFile = os.path.join(outputDirectory, inputFile)
    print(readFromFile)
    print(addInfoFile)
    if (os.path.isfile(readFromFile)):
        if(os.path.isfile(addInfoFile)):
            with open(readFromFile, 'rb') as fsrc:
                with open(addInfoFile, 'wb') as fdest:
                    shutil.copyfileobj(fsrc, fdest, 1000)




def addUpdatedDate(inputDirectory,inputFile,digest,newDate):
    print("Dates are different but digest same, updating date to earliest")

    with open(os.path.join(inputDirectory, '.sync')) as jsonData:
        jsonDict = json.load(jsonData)

    newDict = defaultdict(str,jsonDict)

    newDict[inputFile].insert(0, (newDate, digest))

    with open((os.path.join(inputDirectory, '.sync')), 'w') as outfile:
        json.dump(newDict, outfile,indent=4)

def getMostRecentDate(fileOne, fileTwo):
    fileOneTime = datetime.strptime(fileOne[0], "%Y-%m-%d %H:%M:%S %z")
    fileTwoTime = datetime.strptime(fileTwo[0], "%Y-%m-%d %H:%M:%S %z")
    #return true if file one is the earliest
    if fileOneTime < fileTwoTime:
        return True
    else:
        #return false if false two is earliest
        return False

def updateToLatest(dirOneFile,dirTwoFile):
    pass


if __name__ == "__main__":
    checkInputDirectories()
    createSyncFile(firstDirectory)
    createSyncFile(secondDirectory)
    updateSyncFile(firstDirectory)
    compareDirectories()


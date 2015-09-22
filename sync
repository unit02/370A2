#!/usr/bin/env python3

import sys
import os
import shutil
import json
import time
import hashlib
from collections import defaultdict
from datetime import datetime as dateTime

firstDirectory = sys.argv[1]
secondDirectory = sys.argv[2]


def checkInputDirectories():
    #Neither of the inputs are directories
    if not (os.path.isdir(firstDirectory)) and not ( os.path.isdir(secondDirectory)):
        print("Those aren't directories!")
        return False

    #The first directory is real, must create second one
    elif (os.path.isdir(firstDirectory)) and not ( os.path.isdir(secondDirectory)):
        createNewDirectory(secondDirectory)
        copyFilesInDirectory(firstDirectory,secondDirectory)
        return True


    #The second directory is real, must create first one
    elif not (os.path.isdir(firstDirectory)) and ( os.path.isdir(secondDirectory)):
        createNewDirectory(firstDirectory)
        copyFilesInDirectory(secondDirectory,firstDirectory)
        return True

    return True

def createNewDirectory(directoryToMake):
    os.makedirs(directoryToMake)

def copyFilesInDirectory(inputDirectory,outputDirectory):
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

        if not (os.path.isfile(fullName)):
            if jsonDict[file][0][1] != "Deleted":
                mod = time.strftime("%Y-%m-%d %H:%M:%S %z" , time.gmtime())
                newDict[file].insert(0, (mod, "Deleted"))
            continue

        newDigest = encodeFile(fullName)

        if not newDigest == jsonDict[file][0][1]:
            modTime = os.path.getmtime(fullName)
            mod = time.strftime("%Y-%m-%d %H:%M:%S %z" , time.localtime(modTime))
            newDict[file].insert(0, (mod, newDigest))

    #add in any files not already in file
    fileList = os.listdir(inputDirectory)
    for file in fileList:
        if not file.startswith('.') and not file.endswith('~') :
            fullName = os.path.join(inputDirectory, file)
            if (os.path.isfile(fullName)):
                digest = encodeFile(fullName)
                if file not in newDict:
                    newDict[file] = []
                    modTime = os.path.getmtime(fullName)
                    mod = time.strftime("%Y-%m-%d %H:%M:%S %z", time.localtime(modTime))
                    newDict[file].append((mod, digest))

    with open((os.path.join(inputDirectory, '.sync')), 'w') as outfile:
        json.dump(newDict, outfile,indent=4)

def getDirectorySyncInfo(directory):
        with open(os.path.join(directory, '.sync')) as jsonData:
            dirJson = json.load(jsonData)
        return dirJson

def addOldFileInfo(fileInfo,jsonDict, inputDirectory,fileName):
    print("Add ofld file")
    date = fileInfo[0][0]
    digest = fileInfo[0][1]
    jsonDict[fileName]= []
    jsonDict[fileName].append((date,digest))
    print("adding this date to the digest")
    print(date)
    with open((os.path.join(inputDirectory, '.sync')), 'w') as outfile:
        json.dump(jsonDict, outfile,indent=4)

def checkIfDateDiff(file,fileOne,fileTwo,directoryOne,directoryTwo):
    if fileOne[0] != fileTwo[0]:
        mostRecentIsOne = getMostRecentDate(fileOne,fileTwo)
        if not(mostRecentIsOne):
            addUpdatedDate(directoryTwo, file,fileTwo[1],fileOne[0])
        else:
            addUpdatedDate(directoryOne, file,fileOne[1],fileTwo[0])
        return True
    return False

def checkAndCompareSyncFiles(directoryOne,directoryTwo):
    dirOneJson = getDirectorySyncInfo(directoryOne)
    dirTwoJson = getDirectorySyncInfo(directoryTwo)

    for file in dirOneJson:
        fullName = os.path.join(directoryOne, file)
        #if the file is not in the other directory, then add it and update that directories sync file WITH THE MATCHING DATE AND TIME
        #WORK FROM HERE
        #addOlfFileInfo
        if file not in dirTwoJson and(os.path.isfile(fullName)):
            #needs to copy metadata
            shutil.copy2(fullName, directoryTwo)
            #just manually add it if it doesnt work
            #do manual add to the json file, adding in old date etc etc
            addOldFileInfo(dirOneJson[file],dirTwoJson,directoryTwo,file)

        else:
            fileOne = dirOneJson[file][0]
            fileTwo = dirTwoJson[file][0]
        #file exists in d2, check date, if diff the, then hash. if diff and date
            dirOneDigest = fileOne[1]
            dirTwoDigest = fileTwo[1]

            #Digests are same, date is diff
            if dirOneDigest == dirTwoDigest:
                #moved to checkifdatesdiff method
                if fileOne[0] != fileTwo[0]:
                    mostRecentIsOne = getMostRecentDate(fileOne,fileTwo)
                    if not(mostRecentIsOne):
                        addUpdatedDate(directoryTwo, file,dirTwoDigest,fileOne[0])
                    else:
                        addUpdatedDate(directoryOne, file,dirOneDigest,fileTwo[0])

            elif(dirOneDigest == "Deleted"):
                pathToFile = os.path.join(directoryTwo, file)
                os.remove(pathToFile)
            else:
                print("digests are different")
                print("file one date is ")
                print(fileOne[0])
                print("file two date is ")
                print(fileTwo[0])
                #digests are different, if dates are different get the most recent one and replace the other file
                mostRecentIsOne = getMostRecentDate(fileOne,fileTwo)
                if(mostRecentIsOne):
                    print("most recent is one")
                    print(file)
                    copyFileInfo(file,directoryOne,directoryTwo)
                    updateSyncFile(directoryOne)
                    updateSyncFile(directoryTwo)
                    #the first file is newest, so replace the contents of file two with file one
                else:
                    print("most recent is two")
                    print(file)
                    print(fileOne)
                    print(fileTwo)
                    copyFileInfo(file,directoryTwo,directoryOne)

                    updateSyncFile(directoryOne)
                    updateSyncFile(directoryTwo)

def compDir():
    updateSyncFile(firstDirectory)
    updateSyncFile(secondDirectory)
    checkAndCompareSyncFiles(firstDirectory,secondDirectory)
    checkAndCompareSyncFiles(secondDirectory,firstDirectory)


def compareDirectories():
    updateSyncFile(firstDirectory)
    updateSyncFile(secondDirectory)

    with open(os.path.join(firstDirectory, '.sync')) as jsonData:
        dirOneJson = json.load(jsonData)

    with open(os.path.join(secondDirectory, '.sync')) as jsonDataTwo:
        dirTwoJson = json.load(jsonDataTwo)

    for file in dirOneJson:
        fullName = os.path.join(firstDirectory, file)
        if file not in dirTwoJson and(os.path.isfile(fullName)):
            shutil.copy2(fullName, secondDirectory)
            #do manual add to the json file, adding in old date etc etc
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
                    if not(mostRecentIsOne):
                        addUpdatedDate(secondDirectory, file,dirTwoDigest,fileOne[0])
                    else:
                        addUpdatedDate(firstDirectory, file,dirOneDigest,fileTwo[0])
            elif(dirOneDigest == "Deleted"):
                pathToFile = os.path.join(secondDirectory, file)
                os.remove(pathToFile)
            else:
                #Files are different, if dates are different get the most recent one and replace the other file
                mostRecentIsOne = getMostRecentDate(fileOne,fileTwo)
                if(mostRecentIsOne):
                    print("first most recent is one")
                    print(fullName)
                    copyFileInfo(file,secondDirectory,firstDirectory)
                    updateSyncFile(firstDirectory)
                    updateSyncFile(firstDirectory)
                    #the first file is newest, so replace the contents of file two with file one
                else:
                    print(fullName)
                    print("first most recent is two")
                    copyFileInfo(file,firstDirectory,secondDirectory)
                    updateSyncFile(secondDirectory)

    for file in dirTwoJson:
        fullName = os.path.join(secondDirectory, file)
        if file not in dirOneJson:
            shutil.copy(fullName, firstDirectory)
            updateSyncFile(firstDirectory)
        else:
            fileOne = dirOneJson[file][0]
            fileTwo = dirTwoJson[file][0]
        #file exists in d1, check date, if diff the, then hash. if diff and date
            dirOneDigest = fileOne[1]
            dirTwoDigest = fileTwo[1]
            #Digests are same, date is diff
            if dirOneDigest == dirTwoDigest:
                if fileOne[0] != fileTwo[0]:
                    mostRecentIsOne = getMostRecentDate(fileOne,fileTwo)
                    if not (mostRecentIsOne):
                        addUpdatedDate(secondDirectory, file,dirTwoDigest,fileOne[0])
                    else:
                        addUpdatedDate(firstDirectory, file,dirOneDigest,fileTwo[0])
            elif(dirTwoDigest == "Deleted"):
                pathToFile = os.path.join(firstDirectory, file)
                os.remove(pathToFile)
            else:
                #Files are different, if dates are different get the most recent one and replace the other file
                mostRecentIsOne = getMostRecentDate(fileOne,fileTwo)
                if(mostRecentIsOne):
                    print("sec most recent is one")
                    print(fullName)
                    copyFileInfo(file,secondDirectory,firstDirectory)

                    updateSyncFile(firstDirectory)
                    #the first file is newest, so replace the contents of file two with file one
                else:
                        print("sec most recent is else")
                        print(fullName)
                        copyFileInfo(file,firstDirectory,secondDirectory)
                        updateSyncFile(secondDirectory)


def copyFileInfo(inputFile,inputDirectory,outputDirectory):
    readFromFile = os.path.join(inputDirectory, inputFile)
    addInfoFile = os.path.join(outputDirectory, inputFile)
    print("copying from to")
    print(readFromFile)
    print(outputDirectory)
    shutil.copy2(readFromFile, outputDirectory)

    '''if (os.path.isfile(readFromFile)):
        if(os.path.isfile(addInfoFile)):
            with open(readFromFile, 'rb') as fsrc:
                with open(addInfoFile, 'wb') as fdest:
                    shutil.copyfileobj(fsrc, fdest, 1000)'''

def addUpdatedDate(inputDirectory,inputFile,digest,newDate):
    with open(os.path.join(inputDirectory, '.sync')) as jsonData:
        jsonDict = json.load(jsonData)
    newDict = defaultdict(str,jsonDict)

    newDict[inputFile].insert(0, (newDate, digest))

    with open((os.path.join(inputDirectory, '.sync')), 'w') as outfile:
        json.dump(newDict, outfile,indent=4)

def getMostRecentDate(fileOne, fileTwo):

    fileOneTime = time.mktime(time.strptime(fileOne[0], "%Y-%m-%d %H:%M:%S %z"))
    fileTwoTime = time.mktime(time.strptime(fileTwo[0], "%Y-%m-%d %H:%M:%S %z"))
    #return true if file one is the earliest
    if fileOneTime > fileTwoTime:
        return True
    else:
        #return false if false two is earliest
        return False

if __name__ == "__main__":

    if(checkInputDirectories()):
        syncFile = os.path.join(firstDirectory, '.sync')
        if not(os.path.isfile(syncFile)):
            createSyncFile(firstDirectory)
        syncFileTwo = os.path.join(secondDirectory, '.sync')
        if not(os.path.isfile(syncFileTwo)):
            createSyncFile(secondDirectory)
        updateSyncFile(firstDirectory)
        updateSyncFile(secondDirectory)
        compDir()



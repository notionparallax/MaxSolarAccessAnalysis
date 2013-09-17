from operator import itemgetter, attrgetter
import os
import msaClasses as msac

def uniqueItems(seq, idfun=None): 
   # order preserving
   # taken from http://www.peterbe.com/plog/uniqifiers-benchmark
   if idfun is None:
       def idfun(x): return x
   seen = {}
   result = []
   for item in seq:
       marker = idfun(item)
       if marker in seen: continue
       seen[marker] = 1
       result.append(item)
   return result

def pullNamesFromFolder(dirList):
    files = []
    for fname in dirList:
        name = fname.split(".png")
        if len(name) >1:
            n = fname.split("_")
            files.append({n[0]:n[1],
                          n[2]:n[3],
                          n[4]:n[5],
                          n[6]:n[7],
                          n[8]:n[9]})
    return files

def filenamesToObjects(files):
    saImages = []
    for img in files:
        saImages.append(msac.saImage(img['hr'],
                                img['faceID'],
                                img['min'],
                                img['name'],
                                img['month']))
    return saImages

def sortOnMultipleKeys(thingToSort, tupleOfKeysAsStrings):
    for key in tupleOfKeysAsStrings:
        #this is probably no different to sort.thing
        #how do I avoid side effects?
        thingToSort = sorted(thingToSort, key=attrgetter(key))
    return thingToSort

def getFileList(path, sortOrder):
    #get the filenames from the folder
    dirList=os.listdir(path)

    #chop up the filenames and make them prettier
    files = pullNamesFromFolder(dirList)

    #push the chopped up filenames into objects
    saImages = filenamesToObjects(files)

    #sort images
    saImages = sortOnMultipleKeys(saImages, sortOrder)

    return saImages

def binByMonth(month, imageList):
    tempMonthBin = []
    for img in imageList:
        if month+1 == img.month:
            tempMonthBin.append(img)
    return tempMonthBin

def binByFace(imagesBinnedByMonth):
    mbin = imagesBinnedByMonth
    faceBins = []
    idBins = uniqueItems((img.faceID for img in mbin))
    for idBin in idBins:
        thisFaceBin = []        
        for img in mbin:
            if img.faceID == idBin:
                thisFaceBin.append(img)        
        faceBins.append(thisFaceBin)
    return faceBins
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


'''
['faceID', 0
 '9',      1
 'Level',  2
 '10',     3
 'Appt',   4 
 'G',      5
 'Win',    6
 '1',      7
 'month',  8
 '6',      9
 'hr',    10
 '9',     11
 'min',   12
 '45',    13
 '.png']  14
'''
def pullNamesFromFolder(dirList):
    files = []
    for fname in dirList:
        name = fname.split(".png")
        if len(name) >1:
            n = fname.split("_")
            files.append({'file_name':fname,
                          n[ 0]:n[ 1],
                          n[ 2]:n[ 3],
                          n[ 4]:n[ 5],
                          n[ 6]:n[ 7],
                          n[ 8]:n[ 9],
                          n[10]:n[11],
                          n[12]:n[13]})
    return files

def filenamesToObjects(files, path):
    saImages = []
    for img in files:
        #this is where the class happens!!!!!!!!!!!!!!!!!!!!!!
        anImage =  msac.saImage(hour   = img['hr'], 
                                faceID = img['faceID'], 
                                minute = img['min'], 
                                #name   = img['name'], 
                                month  = img['month'], 
                                path   = path, 
                                file_name         = img['file_name'],
                                building_level    = img['Level'], 
                                appartment        = img['Appt'], 
                                appartment_window = img['Win']
                               )
        #print anImage
        saImages.append(anImage)
    return saImages

def sortOnMultipleKeys(thingToSort, tupleOfKeysAsStrings):
    for key in tupleOfKeysAsStrings:
        #this is probably no different to sort.thing
        #how do I avoid side effects?
        if key in thingToSort:
            thingToSort = sorted(thingToSort, key=attrgetter(key))
    return thingToSort

def getFileList(path, sortOrder):
    #get the filenames from the folder
    dirList=os.listdir(path)
    #print(dirList)
    
    #chop up the filenames and make them prettier
    files = pullNamesFromFolder(dirList)
    #print(files)
    
    #push the chopped up filenames into objects
    saImages = filenamesToObjects(files, path)
    #print(saImages)

    #sort images
    saImages = sortOnMultipleKeys(saImages, sortOrder)
    #print(saImages)
    
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
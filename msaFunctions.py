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
            n = fname.split(".png")[0].split("_")
            
            #overcome the name being _ split too.
            tempName = "-".join([n.pop(3),n.pop(3),n.pop(3),n.pop(3)])
            n.insert(3, tempName)
            
            #print n
            
            files.append({'file_name':fname,
                          n[ 0]:n[ 1],
                          n[ 2]:n[ 3],
                          n[ 4]:n[ 5],
                          n[ 6]:n[ 7],
                          n[ 8]:n[ 9],
                          n[10]:n[11]
                          })
    return files

def filenamesToObjects(files, path):
    saImages = []
    for img in files:
        name = img['name'].split("-")
        nLevel = name[1]
        nAppt  = name[2]
        nWin   = name[3]
        #this is where the class happens!!!!!!!!!!!!!!!!!!!!!!
        anImage =  msac.saImage(hour   = img['hr'], 
                                faceID = img['faceID'], 
                                minute = img['min'], 
                                name   = img['name'], 
                                month  = img['month'], 
                                path   = path, 
                                file_name         = img['file_name'],
                                building_level    = nAppt,#img['Level'], 
                                appartment        = nAppt,#img['Appt'], 
                                appartment_window = nWin,#img['Win']
                                whitePercentage   = img["wpc"],
                                building          = img['name'][0]
                               )
        #print anImage
        saImages.append(anImage)
    return saImages

def sortOnMultipleKeys(thingToSort, tupleOfKeysAsStrings):
    try:
        #('minute','hour','appartment_window','appartment','building_level','month')
        return sorted(thingToSort, key=attrgetter(*tupleOfKeysAsStrings))                
    except AttributeError, e:
        print str(e)

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
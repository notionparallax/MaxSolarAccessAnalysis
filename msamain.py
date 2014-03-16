print ('GO!!')
import datetime
import string

from msaFunctions import *
import msaTemplates as msat
#from msaClasses import saImage

"""
File name format was:
faceID_1_name_Diversity-Wall_month_1_hr_7_min_15_.png
now
faceID_1_name_Level_10_Appt_A_Win_1_month_6_hr_7_min_0_.png
"""
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

months = [  'January'  ,            'February' ,            'March'    ,
            'April'    ,            'May'      ,            'June'     ,
            'July'     ,            'August'   ,            'September',
            'October'  ,            'November' ,            'December' ]

#############################################################################

#Action starts here:
path='C:\\Users\\bdoherty\\Desktop\\AMP_solar'
print(path)
print

numberOfHoursToPass = 2
numberOfImagesPerHour = 4      
bracketStartTime =  9
BracketEndTime   = 15  
print "numberOfHoursToPass", numberOfHoursToPass, "numberOfImagesPerHour", numberOfImagesPerHour, "bracketStartTime", bracketStartTime, "BracketEndTime", BracketEndTime
print

#gets, formats into objects and sorts the filenames
saImages = getFileList(path, ('minute','hour','appartment_window',
                              'appartment','building_level','month'))

appts={}
for i in saImages:
    if i.name in appts:
        appts[i.name] +=1
    else:
        appts[i.name] =1
#print appts

#explicity name the appts
buildingA = []
buildingB = []
buildingC = []


for name in appts.keys():
    if name[0] == "A":
        buildingA.append(name)
    if name[0] == "B":
        buildingB.append(name)
    if name[0] == "C":
        buildingC.append(name)
    else:
        print "someting strange afoot in",name 

for building in [buildingA, buildingB, buildingC]:
    ##get an outputfile ready
    outputFileName = '\checkingList_'+building[0][0]+'.html'
    open(path + outputFileName, 'w').close()
    
    f = open(path + outputFileName, 'a')
    print f
    
    
    #make the header, as far as putting a title into the doc
    f.write( msat.headTmpl.render(
        variable = 'Visualising solar access to these faces',
        when = datetime.date.today() ) )
    
    #build out a square array of rows
    rows=[]
    month = 6
    for apartment in building:        
        apptDetails = apartment.split("-")
        bld   = apptDetails[0] #a letter; A, B or C
        level = int(apptDetails[1], base=10 )
        appt  = int(apptDetails[2], base=10 )
        win   = int(apptDetails[3], base=10 )
        
        
        r = [x for x in saImages if x.name == apartment]
        #x.building == bld and x.building_level == level and x.appartment == appt and x.appartment_window == win]
        
        #print  apartment, len(r)

        r = sortOnMultipleKeys(r, ('hour','minute'))  
        #if len(r)>0: 
        #    print "building",building[0][0],"level", level, "appt", appt, "win", win 
        #    print len(r)#, r[0]
        rows.append(r)            
    
    example = { "ID": 90, "min": 45, "hour": 19, "month":  6, "path": "C:\\Users\\bdoherty\\Desktop\\AMP_solar", 
                "name": "C-11-6-1", "filename": "faceID_90_name_C_11_6_1_month_6_hr_19_min_45_wpc_0.0.png", 
                "building_level": 6, "appartment": "6", "appartment_window": 1, "pcWhite": 0.0, "building": "C" }

    def sortcriteria(aRow):
        #print aRow
        x = aRow[0]
        #print x
        sortString = str(x.building_level)+str(x.appartment)+str(x.appartment_window)
        #print sortString
        sorter =int(sortString, base=10) 
        print sorter, type(sorter)
        return sorter
    
    rowsWithIDs=[]
    for r in rows:
        rowsWithIDs.append({"level":r[0].building_level,"appt":r[0].appartment,"win":r[0].appartment_window,"row":r})
    
    #sortcriteria(rows[0])
    rows = sorted(rowsWithIDs, key=lambda x:x["win"])
    rows = sorted(rowsWithIDs, key=lambda x:x["appt"])
    rows = sorted(rowsWithIDs, key=lambda x:x["level"])
    #sortOnMultipleKeys(rowsWithIDs,("win","appt","level"))
    
    hardPasses=0
    softPasses=0
    nonZero   =0
    fail      =0
    
    for r in rows:
        r = r["row"]
        if len(r) != 0:
            # count the number of images in each row (one row per window plane) and 
            # put that value in -timeWithAnyLight-, then recount with stricter criteria
            # and put that value into the -timeInBracketWithLight- variable.
            # then translate these numbers into types of pass.
                        
            timeWithAnyLight       = len([img for img in r if  img.pcWhite > 0 ])/numberOfImagesPerHour
            timeInBracketWithLight = len([img for img in r if  img.pcWhite > 0 
                                                            and img.hour >= bracketStartTime 
                                                            and img.hour <= BracketEndTime])/numberOfImagesPerHour
            passStatus = 'unknown'
            if timeInBracketWithLight > numberOfHoursToPass:
                passStatus = "hard-pass"
                hardPasses+=1
            elif timeWithAnyLight     > numberOfHoursToPass:
                passStatus = "soft-pass"
                softPasses+=1
            elif timeWithAnyLight     > 0:
                passStatus = "non-zero"
                nonZero+=1
            elif timeWithAnyLight    == 0:
                passStatus = 'fail'
                fail+=1
            
            window={
                'totalHours'    : timeWithAnyLight,
                'inBracketHours': timeInBracketWithLight,
                'passStatus'    : passStatus
            }
            #print window
            f.write( msat.eachimgTempl.render(row=r, monthNames=months, window=window) )
    
    total = hardPasses + softPasses + nonZero + fail
    resultString =("hardPasses: "+str(hardPasses) + " - " + str(hardPasses/float(total)*100) + "%<br>" +
                   "softPasses: "+str(softPasses) + " - " + str(softPasses/float(total)*100) + "%<br>" +
                   "nonZero   : "+str(nonZero)    + " - " + str(nonZero/float(total)*100) + "%<br>" +
                   "fail      : "+str(fail)       + " - " + str(fail/float(total)*100) + "%<br>")
    print "\n".join(resultString.split('<br>'))
    f.write( msat.tailTmpl.render( variable = resultString))
        
    f.close()

print "done"
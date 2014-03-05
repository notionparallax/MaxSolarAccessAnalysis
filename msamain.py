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
numberOfImagesPerHour = 2      
bracketStartTime =  9
BracketEndTime   = 15  
print "numberOfHoursToPass", numberOfHoursToPass, "numberOfImagesPerHour", numberOfImagesPerHour, "bracketStartTime", bracketStartTime, "BracketEndTime", BracketEndTime
print

#gets, formats into objects and sorts the filenames
saImages = getFileList(path, ('minute','hour','appartment_window',
                              'appartment','building_level','month'))

for building in ["A", "B", "C"]:
    ##get an outputfile ready
    outputFileName = '\checkingList_'+building+'.html'
    open(path + outputFileName, 'w').close()
    
    f = open(path + outputFileName, 'a')
    print f
    
    
    #make the header, as far as putting a title into the doc
    f.write( msat.headTmpl.render(
        variable = 'Visualising solar access to these faces',
        when = datetime.date.today() ) )
    
    #a= [( x.building_level, x.appartment, x.appartment_window) for x in saImages ]
    #print a
    
    #build out a square array of rows
    rows=[]
    #for month in range(5,7):
    month = 6
    for level in range(0,12):
        for appt in range(10):
            for win in range(5):
                #print "building",building,"level", level, "appt", appt, "win", win              
                r = [x for x in saImages if x.building == building and x.building_level == level and x.appartment == appt and x.appartment_window == win]
                r = sortOnMultipleKeys(r, ('hour','minute'))   
                #print r             
                rows.append(r)            
    
    for r in rows:
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
            elif timeWithAnyLight     > numberOfHoursToPass:
                passStatus = "soft-pass"
            elif timeWithAnyLight     > 0:
                passStatus = "non-zero"
            elif timeWithAnyLight    == 0:
                passStatus = 'fail'
            
            window={
                'totalHours'    : timeWithAnyLight,
                'inBracketHours': timeInBracketWithLight,
                'passStatus'    : passStatus
            }
            print window
            f.write( msat.eachimgTempl.render(row=r, monthNames=months, window=window) )
    
    f.write( msat.tailTmpl.render(
        variable = 'Visualising solar access to these faces'
        ))
        
    f.close()

print "done"
print ('GO!!')
import datetime

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
path='./tower_example/6'
print(path)

#gets, formats into objects and sorts the filenames
saImages = getFileList(path, ('minute','hour','Win','Appt','Level','month'))
print(saImages)

for i in saImages:
    print(i)
    #print i.appendPcWhiteToFileName()#this doesn't actually change the file name yet


monthBinnedImages = []
for month in range(len(months)):
    tempMonthBin = binByMonth(month, saImages)
    if len(tempMonthBin) > 0:        
        monthBinnedImages.append(tempMonthBin)

binnedImages = []
for mbin in monthBinnedImages:
    binnedImages.append(binByFace(mbin))
   
#build a string, seems neater than writing to the file a lot
thehtml = ""

#make the header, as far as putting a title into the doc
thehtml += msat.headTmpl.render(
    variable = 'Visualising solar access to these faces',
    when = datetime.date.today()
    )

for moBin in binnedImages:
    if len(moBin)!= 0:
        print moBin
        
        thehtml +=  msat.eachTableTempl.render(
            #amoi is "a month of images"
            monthName = months[int(moBin[0][0].month-1)],
            amoi = moBin,
            img_path = path
        )

thehtml += msat.tailTmpl.render(
    variable = 'Visualising solar access to these faces'
    )

#get an outputfile ready
f = open('tempworkfile.html', 'w')
print thehtml
f.write(thehtml)
f.close()



print "done"
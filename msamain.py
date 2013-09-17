import datetime

from msaFunctions import *
import msaTemplates as msat
#from msaClasses import saImage

"""
File name format is:
faceID_1_name_Diversity-Wall_month_1_hr_7_min_15_.png

"""


months = [  'January'  ,            'February' ,            'March'    ,
            'April'    ,            'May'      ,            'June'     ,
            'July'     ,            'August'   ,            'September',
            'October'  ,            'November' ,            'December' ]

#############################################################################

#Action starts here:
path='C:/Users/bdoherty/Desktop/Max-Analysis/MaxSolarAccessAnalysis/Images'

#gets, formats into objects and sorts the filenames
saImages = getFileList(path, ('minute','hour','faceID','month'))

monthBinnedImages = []
for month in range(len(months)):
    tempMonthBin = binByMonth(month, saImages)
    if len(tempMonthBin) > 0:        
        monthBinnedImages.append(tempMonthBin)

binnedImages = []
for mbin in monthBinnedImages:
    binnedImages.append(binByFace(mbin))
   
#get an outputfile ready
f = open('tempworkfile.html', 'w')

#build a string, seems neater than writing to the file a lot
thehtml = ""

#make the header, as far as putting a title into the doc
thehtml += msat.headTmpl.render(
    variable = 'Visualising solar access to these faces',
    when = datetime.date.today()
    )

#print monthBinnedImages
for moBin in binnedImages:
    if len(moBin)!= 0:
        #
        thehtml +=  msat.eachTableTempl.render(
            #amoi is "a month of images"
            monthName = months[int(moBin[0][0].month-1)],
            amoi = moBin
        )

thehtml += msat.tailTmpl.render(
    variable = 'Visualising solar access to these faces'
    )
print thehtml
f.write(thehtml)
f.close()
#fancy bit to only put in comma if it not the last item
#{% if not loop.last %},{% endif %}
print "done"
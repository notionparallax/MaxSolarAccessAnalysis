import os
from operator import itemgetter, attrgetter
import datetime
from jinja2 import Template

import msaFunctions

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
        saImages.append(saImage(img['hr'],
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

class saImage:
    def __init__(self, hour, faceID, minute, name, month):
        self.hour   = int(hour,   base=10)
        self.faceID = int(faceID, base=10)
        self.minute = int(minute, base=10)
        self.name   = name
        self.month  = int(month,  base=10)
        
    def fileName(self):
        return "faceID_"+str(self.faceID) +\
                "_name_"+str(self.name) +   \
                "_month_"+str(self.month) + \
                "_hr_"+str(self.hour) +     \
                "_min_"+str(self.minute) +  \
                "_.png"
                
    def __repr__(self):
        return repr((' ID: {:2}'.format(self.faceID)+
                        ', min: {:2}'.format(self.minute)+
                        ', hr: {:2}'.format(self.hour)+
                        ', month: {:2}'.format(self.month)+
                        ', name: {:14}'.format(self.name)+
                        ', filename: {}'.format(self.fileName())
                    ))

months = [  'January'  ,            'February' ,            'March'    ,
            'April'    ,            'May'      ,            'June'     ,
            'July'     ,            'August'   ,            'September',
            'October'  ,            'November' ,            'December' ]

#############################################################################

#Action starts here:
path='/home/ben/Dropbox/Public/sites/dataStory/MaxSolarAccessAnalysis/Images'

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
f = open('workfile.html', 'w')
#build a string, seems neater than writing to the file a lot
thehtml = ""

headTmpl = Template(u'''\
<!DOCTYPE html>
<html>
  <head>
    <title>{{ variable|escape }}</title>
    <style>
        img {height:60px;
             border-right-style: solid;
             border-right-width: 1px;
             border-right-color: #C0C0C0}
        .render{width:225px; }
        body{font-family:'HelveticaNeueLT Com 45 Lt', 'Helvetica', Arial}
    </style>
  </head>
  <body>
  <h1>Run at {{ when }}</h1>
  ''')
thehtml += headTmpl.render(
    variable = 'Visualising solar access to these faces',
    when = datetime.date.today()
)

eachTableTempl = Template(u'''\
  <h1>{{monthName}} 21<sup>st</sup></h1>
  <table>
  <tr>
    {%- for img in amoi[0] %}
          <td>
            <p>{{ img.hour }}:{{ '{:2}'.format(img.minute) }}</p>
          <td>
      {%- endfor %}
  </tr>
  <tr>
    {%- for img in amoi[0] %}
          <td>
            <div class="render">
                  <p>{{ img.name|replace("-", " ") }}<br>
                  <img src="Images/{{ img.fileName() }}" /></p>
              </div>
          <td>
      {%- endfor %}
  </tr>

  <tr>
    {%- for img in amoi[0] %}
          <td>
            <div class="render">
                  <p>{{ amoi[1][loop.index-1].name|replace("-", " ") }}<br>                  
                    <img src="Images/{{ amoi[1][loop.index-1].fileName() }}" /><img src="Images/{{ amoi[2][loop.index-1].fileName() }}" />
                  </p>
              </div>
          <td>
      {%- endfor %}
  </tr>
  
  </table>
  
''')
#print monthBinnedImages
for moBin in binnedImages:
    if len(moBin)!= 0: 
        thehtml +=  eachTableTempl.render(
            #amoi is "a month of images"
            monthName = months[int(moBin[0][0].month-1)],
            amoi = moBin
        )

tailTmpl = Template(u'''\
<h3>Disclaimer</h3>
<p>{{ variable|escape }}</p>
  </body>
</html>''')
thehtml += tailTmpl.render(
    variable = 'Visualising solar access to these faces'
)

f.write(thehtml)
f.close()
#fancy bit to only put in comma if it not the last item
#{% if not loop.last %},{% endif %}
print "done"

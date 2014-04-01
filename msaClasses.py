import os
from PIL import Image

class saImage:
    def __init__(self, hour=None, faceID=None, area=None, minute=None, name=None,
                 month=None, path=None, file_name=None, building_level=None,
                 appartment=None, appartment_window=None, whitePercentage=0.0,
                 building="A"):
        self.hour              = int(hour              , base=10)
        self.faceID            = int(faceID            , base=10)
        self.minute            = int(minute            , base=10)
        self.name              = name
        self.month             = int(month             , base=10)
        self.path              = path
        self.filename          = file_name
        self.building          = building
        self.area              = float(area)
        self.building_level    = int(building_level    , base=10 )
        self.appartment        = int(appartment        , base=10)
        self.appartment_window = int(appartment_window , base=10)
        self.pcWhite           = float(whitePercentage) #self.countPx()
        self.exposedArea       = self.exposedArea()

    """
    def fileName(self):
        return "faceID_" + str(self.faceID) +\
                "_name_" + str(self.name)   +\
                "_month_" + str(self.month) +\
                "_hr_" + str(self.hour)     +\
                "_min_" + str(self.minute)  +\
                "_.png"
    """


    def __repr__(self):
        return repr((  '{'+
                        '  "ID": {:2}'.format(self.faceID)+
                        ', "min": {:2}'.format(self.minute)+
                        ', "hour": {:2}'.format(self.hour)+
                        ', "month": {:2}'.format(self.month)+
                        ', "path": "{}"'.format(self.path)+
                        ', "name": "{}"'.format(self.name)+
                        ', "filename": "{}"'.format(self.filename)+
                        ', "building_level": {}'.format(self.building_level)+
                        ', "appartment": "{}"'.format(self.appartment)+
                        ', "appartment_window": {}'.format(self.appartment_window)+
                        ', "pcWhite": {:4}'.format(self.pcWhite)+
                        ', "area": {:4}'.format(self.area)+
                        ', "building": "{}"'.format(self.building)+
                        ', "exposedArea": "{}"'.format(self.exposedArea)+
                        ' }'
                    ))

    def exposedArea(self):
        return self.area * self.pcWhite

    def countPx(self):
        fullName = self.path+'/'+self.filename
        im = Image.open(fullName)
        if im.mode != "RGB":
            #images can be B&W which doesn't store rgb values - consitent response
            im = im.convert("RGB")

        allPx = list(im.getdata()) #this gets a 1d list of tuples (r,g,b)

        whitePx = 0
        for px in allPx:    #go through the list and count the white pixels
            if px[0]== 255:
                whitePx += 1

        pcWhite = float(whitePx)/len(allPx)
        return pcWhite

    def appendPcWhiteToFileName(self):
        splitName = self.fileName().split('.png')
        newFilename = splitName[0] + "pcWhite_" + str(self.pcWhite) + '.png'
        return newFilename

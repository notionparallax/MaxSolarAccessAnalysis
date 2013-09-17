import os
from PIL import Image

class saImage:
    def __init__(self, hour, faceID, minute, name, month, path):
        self.hour      = int(hour,   base=10)
        self.faceID    = int(faceID, base=10)
        self.minute    = int(minute, base=10)
        self.name      = name
        self.month     = int(month,  base=10)
        self.filename  = self.fileName()
        self.path      = path
        self.pcWhite   = self.countPx()
        
    def fileName(self):
        return "faceID_" + str(self.faceID) +\
                "_name_" + str(self.name)    +\
                "_month_" + str(self.month)  +\
                "_hr_" + str(self.hour)      +\
                "_min_" + str(self.minute)   +\
                "_.png"    
            
    def __repr__(self):
        return repr((  ' ID: {:2}'.format(self.faceID)+
                        ', min: {:2}'.format(self.minute)+
                        ', hr: {:2}'.format(self.hour)+
                        ', month: {:2}'.format(self.month)+
                        ', name: {:14}'.format(self.name)+
                        ', filename: {}'.format(self.fileName())+
                        ', path: {}'.format(self.path)
                    ))

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
# -*- coding: utf-8 -*-
from PIL import Image

#this won't allow me to just ask for smile.png for some reason
im = Image.open("./Images/faceID_1_name_Diversity-Wall_month_5_hr_14_min_45_.png")
im = im.convert("RGB")
#some pleasantries
print("info:", im.info)
print("palette:", im.palette)
print("mode :", im.mode)
print("format:", im.format)
#print("string:", im.tostring())

#this gets a 1d list of tuples (r,g,b)
allPx = list(im.getdata())

#go through the list and count the white pixels
whitePx = 0
for px in allPx:
    if px[0]== 255:
        whitePx = whitePx+1

#calculate the % whities
print "num px:       ", len(allPx)
print "num white px: ", whitePx
pcWhite = float(whitePx)/len(allPx)
print str(round(pcWhite,4))+"% white"
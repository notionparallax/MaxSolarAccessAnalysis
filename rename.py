import os
from PIL import Image

def countPx(path,filename):
    fullName = path+'/'+filename
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



path='../Feaso'

dirList=os.listdir(path)

for fname in dirList:
    #from: faceID_202_name_winfaceA_2_5_1_area_9.18923_month_6_hr_15_min_15_.png
    #to:   faceID_202_name_winfaceA_2_5_1_area_9.18923_month_6_hr_15_min_15_wpc_0.0.png
    newfname = fname.split(".png")[0] + "wpc_{}.png".format( countPx(path, fname) )
    os.rename(path+'/'+fname,
    	      path+'/'+newfname)
    print fname, ' ->', newfname

print 'done'

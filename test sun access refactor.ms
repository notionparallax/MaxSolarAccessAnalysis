fileIn "sunAccessFunctions.ms"
print "****************************"

rootFolder = ""
hourSubdiv = 4
startTime = 7
endTime  = 19
startMonth = 1
endMonth = 11
outputWidth = 400 --in pixels
justMakeTheCameras = false
selectionSetname = "toTest"

print "here we go"
	
--set this to be |selection| if you want to set the selection manually
--analysisFaces = selection
analysisFaces = selectionSets[selectionSetname] 

print ("lets get going on " + (analysisFaces.count as string) + " faces")
for month in startMonth to (endMonth +1)  do -- +1 so that it does the last month
(
	$Daylight001.controller.solar_date = solarDateFromMonth(month)
	print ("month " + solarDateFromMonth(month) as string)
	
	for i in 1 to analysisFaces.count do
	(
		thisFace = analysisFaces[i]
		--theNameOfThisFace = formatName(thisFace.name)
		theNameOfThisFace = thisFace.name
		--print "what we know about thisFace is " + thisFace
		if theNameOfThisFace != undefined then
		(
			print ("theNameOfThisFace is " + (theNameOfThisFace as string))
			mycamera  = Targetcamera pos:[0,0,0]
			mycamera.fov = 120
			mycamera.fovType = 1 --1 means measured horizontaly
			mycamera.showcone = true
			mycamera.name = "cam" + theNameOfThisFace as string
			
			width  = getLongEdgeLength thisFace
			height = getShortEdgeLength thisFace
			print ("face is " + (width as string) + " x " + (height as string))        
			verts =         #((getVert thisFace 1),(getVert thisFace 2),(getVert thisFace 3),(getVert thisFace 4))--print ("verts" + verts as string)
			vertsAdded =   ((getVert thisFace 1)+(getVert thisFace 2)+(getVert thisFace 3)+(getVert thisFace 4))--print ("VA " + vertsAdded as string)
			centroidPoint = ((getVert thisFace 1)+(getVert thisFace 2)+(getVert thisFace 3)+(getVert thisFace 4))/4--print     ("CP " + centroidPoint as string)
			
			aspectRatio = width/height
			renderwidth  = outputWidth
			renderHeight = (1/aspectRatio) * outputWidth
			b = BitMap renderwidth renderHeight color:red    
			eyeDistance = ((width/2)/tan(120/2))--print ("eyeDistance " + eyeDistance as string)
			
			myNormal = getFaceNormal thisFace 1--print myNormal
			eyePoint = centroidPoint + (myNormal*eyeDistance)--print ("eyePoint " + eyePoint as string)    
			tarPoint  = centroidPoint--print ("tarPoint " + tarPoint as string)        
			
			mycamera.position = eyePoint
			mycamera.target = Targetobject pos:tarPoint
			
			--makedir (rootFolder + theNameOfThisFace)			
			if justMakeTheCameras == false then
			(	
				for hour in startTime to endTime do 
				(
					for hourdiv in 0 to hourSubdiv-1 do 
					(
						minutes = (60/hourSubdiv) * hourdiv 
						seconds = 0 
						solTime = SolarTimeFromTime hour minutes
						print solTime as string
						
						$Daylight001.controller.solar_time.controller.value = solTime    
						filename = "faceID_"+ (i as string) +"_name_" + theNameOfThisFace + "_month_" + month as string + "_hr_" + hour as string + "_min_" + minutes as string + "_.png" --name_hr_min.png
						print ("Path details")
						print (rootFolder)
						print (filename)
						fullPath = (rootFolder + filename)
						print (fullPath)
						if doesFileExist(fullPath) then
						(
							print (fullPath as string + "  already exists!! I'll skip this one.")
						)
						else
						(                        
							print fullPath
							b.filename = fullPath                    
							render camera:mycamera to:b vfb:false    
							save b
						)						
					)					
				)
				print "done all the renders for this face"
				gc() --should do a tidy up of the memory
			)
		)
		else
		(
			print "OHSHIT: theNameOfThisFace is undefined"
		)
	)
)
Print "*****finished*****"
fileIn "sunAccessFunctions.ms"
print "****************************"

out_name = GetSaveFileName()
rootFolder = "C:/analysisTest/"
hourSubdiv = 5
startTime = 7
endTime  = 19
outputWidth = 150 --in pixels
justMakeTheCameras = false
selectionSetname = "toTest"

--check that there is a valid file name for creating the html document into
if out_name != undefined then
(
	print "here we go"
	
	--**********************write html to the header***************************
	out_file = createfile out_name --create a file ready to start writing to it

	--This is an HTML header that starts off the table   
	head =  HTMLheader ("Sunlight Study - Winter Solstice "+ (startTime as string) + " to" + (endTime as string))
	title = HTMLtitle "ACTIVE BorrowdaleHouse RENDER ORIGINAL DA" 1
	tableStart = HTMLstartTable "ignoreThisArg" --start the table with an empty cell in the top left corner
	format "%" (head + title + tableStart) to:out_file
		
	--writes out the top line 
	topline = makeTopRow startTime endTime hourSubdiv
	format "%" topline to:out_file --once the loop is finished close the row 
	--********************** end write html to the header***************************
		
	--set this to be |selection| if you want to set the selection manually
	--analysisFaces = selection
	analysisFaces = selectionSets[selectionSetname] 
	
	print ("lets get going on " + (analysisFaces.count as string) + " faces")
	for i in 1 to analysisFaces.count do
	(
		thisFace = analysisFaces[i]
		--theNameOfThisFace = formatName(thisFace.name)
		theNameOfThisFace = thisFace.name + " " + (i as string)
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
			verts =     #((getVert thisFace 1),(getVert thisFace 2),(getVert thisFace 3),(getVert thisFace 4))--print ("verts" + verts as string)
			vertsAdded = ((getVert thisFace 1)+(getVert thisFace 2)+(getVert thisFace 3)+(getVert thisFace 4))--print ("VA " + vertsAdded as string)
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
			format "%" "<tr>" to:out_file
			format "%" ("<td>"+ theNameOfThisFace +"</td>") to:out_file
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
						--print (TimeFromSolarTime solTime) as string
						$Daylight001.controller.solar_time.controller.value = solTime    
						filename = theNameOfThisFace + "_" + hour as string + "_" + minutes as string + ".png" --name_hr_min.png
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
						td = "<td><img src=\""+filename+"\"  width=\"150px\"/></td>\n" 
						format "%" td to:out_file
						--for example
						--<td><img src="windowCaptures/N_1801_T_T/N_1801_T_T_3_10_0.jpg" /></td> 
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
format "%" "</table></body></html>" to:out_file
close out_file
Print "*****finished*****"
)
else
(
	print "out_name is undefined"
)
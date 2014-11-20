print "****************************"

out_name = GetSaveFileName()
rootFolder = "C:/Ben/borrowdale/4timesAnHour/"
hourSubdiv = 4		
startTime = 8
endTime  = 17
outputWidth = 300 --in pixels
justMakeTheCameras = false

--check that there is a valid file name for creatign the html document into
if out_name != undefined then
(
	out_file = createfile out_name                                                                                  --create a file ready to start writing to it
	--This is an HTML header that starts off the table
	format "%" "<!DOCTYPE html>" to:out_file                                                                   --html 5 doctype
	format "%" "<head>" to:out_file                                                                                --
	format "%" "  <title>Sunlight Study - Winter Solstice -09:00 to 15:00</title>" to:out_file    --header
	format "%" "</head>" to:out_file                                                                               --
	format "%" "<body>" to:out_file                                                                                --start body of html
	format "%" "  <h1>ACTIVE BorrowdaleHouse RENDER ORIGINAL DA</h1>" to:out_file           --page title
	format "%" "    <table>" to:out_file                                                                            --start the table
	format "%" "      <tr>" to:out_file                                                                              --start a table row
	format "%" "        <td></td>" to:out_file                                                                    --an empty cell in the top left corner
	--writes out the top line
	for hour in startTime to endTime do 
	(
		for hourdiv in 0 to hourSubdiv-1 do 
		(
			--this writes out a table cell in the top row with the times that will be tested
			--this loop is identical to the next one
			minutes = (60/hourSubdiv) * hourdiv 								
			format "<td>%:%</td>\n" hour  minutes  to:out_file
		)
	)
	format "%" "</tr>" to:out_file --once the loop is finished close the row 

	analysisFaces = selection--Sets["faces to turn into cameras"]	
	print ("lets get going on " + (analysisFaces.count as string) + " faces")

-- 	mycamera  = Targetcamera pos:[0,0,0]
-- 	mycamera.fov = 120
-- 	mycamera.fovType = 1 --1 means measured horizontaly
-- 	mycamera.showcone = true

	for i in 1 to analysisFaces.count do
	(
		thisFace = analysisFaces[i]
		theNameOfThisFace = getName(thisFace.name)
		
	    mycamera  = Targetcamera pos:[0,0,0]
	    mycamera.fov = 120
	    mycamera.fovType = 1 --1 means measured horizontaly
	    mycamera.showcone = true
		mycamera.name = "cam" + theNameOfThisFace as string
		
		width  = getLongEdgeLength thisFace --print ("width " + width as string)
		height = getShortEdgeLength thisFace --print ("height " + height as string)		
		print ("face is " + (width as string) + " x " + (height as string))		
		verts = 	#((getVert thisFace 1),(getVert thisFace 2),(getVert thisFace 3),(getVert thisFace 4))--print ("verts" + verts as string)
		vertsAdded = ((getVert thisFace 1)+(getVert thisFace 2)+(getVert thisFace 3)+(getVert thisFace 4))--print ("VA " + vertsAdded as string)
		centroidPoint = ((getVert thisFace 1)+(getVert thisFace 2)+(getVert thisFace 3)+(getVert thisFace 4))/4--print 	("CP " + centroidPoint as string)
		
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
		
		print theNameOfThisFace
		--makedir (rootFolder + theNameOfThisFace)
		format "%" "<tr>" to:out_file
		format "%" ("<td>"+ theNameOfThisFace +"</td>") to:out_file
		if	justMakeTheCameras == false then
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
					fullPath = rootFolder filename
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
					format "<td><img src=\"%%\"  width=\"150px\"/></td>\n" filename  to:out_file
					--for example
					--<td><img src="windowCaptures/N_1801_T_T/N_1801_T_T_3_10_0.jpg" /></td> 
				)
			)
			--re-place the camera as a locator
			eyePoint = (centroidPoint + (myNormal*600))+[0,0,500]--print ("eyePoint " + eyePoint as string)	
			tarPoint  = [8500,23000,1800]
			mycamera.position = eyePoint
		    mycamera.target = Targetobject pos:tarPoint
			thisAppt = execute("$"+theNameOfThisFace)
			thisAppt.material = meditMaterials[12]
			filename = theNameOfThisFace +"_Locator"+".jpg"
			fullPath = rootFolder + filename 
			if doesFileExist(fullPath) then
			(
				print (fullPath as string + "  already exists!!")
			)
			else
			(						
				print fullPath
				b.filename = fullPath					
				render camera:mycamera to:b vfb:false	
				save b
			)
			thisAppt.material = meditMaterials[14]
			format "<td><img src=\"%%\"  width=\"150px\"/></td>\n" filename  to:out_file
			format "%" "</tr>\n" to:out_file
			gc() --should do a tidy up of the memory
		)
	)
format "%" "</table></body></html>" to:out_file
close out_file
Print "*****finished*****"
)

fn getLongEdgeLength aRectangularFace =
(
	--should return the second longest number, longest is the diagonal
	f = aRectangularFace
	d1  = distance (getVert f 1) (getVert f 2)
	d2  = distance (getVert f 1) (getVert f 3)
	d3  = distance (getVert f 1) (getVert f 4)
	sorted = sort #(d1,d2,d3)
	return sorted [2]
)
fn getShortEdgeLength aRectangularFace =
(
	--should return the second longest number, longest is the diagonal
	f = aRectangularFace
	d1  = distance (getVert f 1) (getVert f 2)
	d2  = distance (getVert f 1) (getVert f 3)
	d3  = distance (getVert f 1) (getVert f 4)
	sorted = sort #(d1,d2,d3)
	return sorted [1]
)

fn getName thingWithAname = 
(
	newName = ((filterString thingWithAname "_")[2])
	return newName
)

fn TimeFromSolarTime solar_time = 
(
	hrs = int(solar_time/3600.0) -- full hours in the solar_time value
	min = int((solar_time - hrs*3600.0)/60.0) -- full minutes in the difference between the full time and the full hours
	sec = int(solar_time - hrs*3600.0 - min*60.0 + 0.5) -- full seconds in the rest of the value
	solar_array = #(hrs,min,sec) -- return the result as a 3 elements array
	return(solar_array) 
)

fn SolarTimeFromTime hrs min = 
(
	solarHrs = hrs 
	solarMin = min/60.0
	--solarSec = 
	sotalTime = solarHrs+solarMin--+solarSec
	return(sotalTime) 
)
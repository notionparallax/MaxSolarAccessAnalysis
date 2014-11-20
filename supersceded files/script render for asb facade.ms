print "****************************"

rootFolder = "C:/Users/bdoherty/Desktop/asb_facade/nonPerforatedBlades/"
hourSubdiv = 1		
startTime = 6
endTime  = 18
startDay = -171
endDay = 193
outputWidth = 800 --in pixels
aspectRatio = 16/9
uniqueID = 100000

for month in 1 to 12 do
(
	day = (monthArray month)-171
	for hour in startTime to endTime do 
	(
		for hourdiv in 0 to hourSubdiv-1 do 
		(
			minutes = (60/hourSubdiv) * hourdiv 
			seconds = 0 
			solTime = SolarTimeFromTime hour minutes
			--print solTime as string
			--print (TimeFromSolarTime solTime) as string
			$Daylight001.controller.solar_date = day
			$Daylight001.controller.solar_time.controller.value = solTime
			
			filename = "ID_" + uniqueID as string + "_DOY_" + (day+171) as string +"_1stOf" + monthName (day+171) as string + "_("+ hour as string + "_" + minutes as string + ").png" 
			fullPath = rootFolder + filename
			if doesFileExist(fullPath) then
			(
				print (fullPath as string + "  already exists!! I'll skip this one.")
			)
			else
			(						
				print fullPath
				
				renderwidth  = outputWidth
				renderHeight = (1/aspectRatio) * outputWidth
				b = BitMap renderwidth renderHeight color:red
				
				b.filename = fullPath					
				render camera:$Camera001 to:b vfb:false	
				save b
			)
			uniqueID = uniqueID+1
		)
	)	
	gc() --should do a tidy up of the memory		
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

fn monthName dayOfTheYear =
(
		 if dayOfTheYear <= 31  then ( return "__" + (dayOfTheYear -   0) as string + "_January") 
	else if dayOfTheYear <= 59  then ( return "__" + (dayOfTheYear -  31) as string + "_February") 
	else if dayOfTheYear <= 90  then ( return "__" + (dayOfTheYear -  59) as string + "_March") 
	else if dayOfTheYear <= 120 then ( return "__" + (dayOfTheYear -  90) as string + "_April") 
	else if dayOfTheYear <= 151 then ( return "__" + (dayOfTheYear - 120) as string + "_May") 
	else if dayOfTheYear <= 181 then ( return "__" + (dayOfTheYear - 151) as string + "_June") 
	else if dayOfTheYear <= 212 then ( return "__" + (dayOfTheYear - 181) as string + "_July") 
	else if dayOfTheYear <= 243 then ( return "__" + (dayOfTheYear - 212) as string + "_August") 
	else if dayOfTheYear <= 271 then ( return "__" + (dayOfTheYear - 243) as string + "_September") 
	else if dayOfTheYear <= 304 then ( return "__" + (dayOfTheYear - 271) as string + "_October") 
	else if dayOfTheYear <= 334 then ( return "__" + (dayOfTheYear - 304) as string + "_November") 
	else if dayOfTheYear <= 365 then ( return "__" + (dayOfTheYear - 334) as string + "_December") 
	else                             ( return "_What is wrong with you?") 
)

fn monthArray1 theMonth =
(
	theMonth = toLower(theMonth as string)
		 if (theMonth == "1"  or theMonth == "january"   or theMonth == "jan") then (return   0)
	else if (theMonth == "2"  or theMonth == "february"  or theMonth == "feb") then (return  31)
	else if (theMonth == "3"  or theMonth == "march"     or theMonth == "mar") then (return  59)
	else if (theMonth == "4"  or theMonth == "april"     or theMonth == "apr") then (return  90)
	else if (theMonth == "5"  or theMonth == "may"       or theMonth == "may") then (return 120)
	else if (theMonth == "6"  or theMonth == "june"      or theMonth == "jun") then (return 151)
	else if (theMonth == "7"  or theMonth == "july"      or theMonth == "jul") then (return 181)
	else if (theMonth == "8"  or theMonth == "august"    or theMonth == "aug") then (return 212)
	else if (theMonth == "9"  or theMonth == "september" or theMonth == "sep") then (return 243)
	else if (theMonth == "10" or theMonth == "october"   or theMonth == "oct") then (return 271)
	else if (theMonth == "11" or theMonth == "november"  or theMonth == "nov") then (return 304)
	else if (theMonth == "12" or theMonth == "december"  or theMonth == "dec") then (return 334)
	else                               ( return "_What is wrong with you?") 
)
fn monthArray theMonth =
(
	theMonth = toLower(theMonth as string)
		 if (theMonth == "1"  ) then (return   0)
	else if (theMonth == "2"  ) then (return  31)
	else if (theMonth == "3"  ) then (return  59)
	else if (theMonth == "4"  ) then (return  90)
	else if (theMonth == "5"  ) then (return 120)
	else if (theMonth == "6"  ) then (return 151)
	else if (theMonth == "7"  ) then (return 181)
	else if (theMonth == "8"  ) then (return 212)
	else if (theMonth == "9"  ) then (return 243)
	else if (theMonth == "10" ) then (return 271)
	else if (theMonth == "11" ) then (return 304)
	else if (theMonth == "12" ) then (return 334)
	else                             ( return "_What is wrong with you?") 
)
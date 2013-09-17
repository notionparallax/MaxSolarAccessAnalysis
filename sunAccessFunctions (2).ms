print "start loading functions"
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

fn formatName thingWithAname = 
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

fn solarDateFromMonth monthInt =
(	
	-- jan 21st = (-151) dec 21st = (183) 
	-- the excel function ROUND((30.357*A2)-181.98,0) produces *almost* the right results, but because of the month length variation it looks like the most eficient way to do this is with an array of dates.
	-- this gives the 21st for each month
	-- this is true for 2013, probably not for any other date.
	--              1     2    3    4    5  6   7   8   9   10   11   12      
	solDate = #( -151, -120, -92, -61, -31, 0, 30, 61, 92, 122, 151, 183)
	return solDate[monthInt]
)

fn HTMLheader titleText =
(
	h = ""
	h = h + "<!DOCTYPE html>"
	h = h + "<html>"
	h = h + "<head>"
	h = h + "<title>"
	h = h + (titleText as string)
	h = h + "</title>"
	h = h + "<style type=\"text/css\">img{height: 60px;}.plantWall{width: 225px;}</style>"
	h = h + "</head>"
    return h
)
fn HTMLtitle headingText Hlevel =
(
    return "  <h" + (Hlevel as string) + ">" + (headingText as string) + "</h" + (Hlevel as string) + ">"
)
fn HTMLstartTable trickArg =
(
    return ("<table>" + "<tr>" + "<td></td>") as string
)

fn MakeTopRow startTime endTime hourSubdiv =
(
    localRow = ""
    for hour in startTime to endTime do 
    (
        for hourdiv in 0 to hourSubdiv-1 do 
        (
            --this writes out a table cell in the top row with the times that will be tested
            minutes = (60/hourSubdiv) * hourdiv
            localRow = localRow + ("<td>"+(hour as string)+":"+(minutes as string)+"</td>\n")
        )
    )
    localRow = localRow + ("</tr>") --once the loop is finished close the row 
    return localRow
)
print "end loading functions"
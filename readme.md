#Solar analysis in 3DSMax
This is a simple workflow for assessing solar access on surfaces. It is mainly used for Australian SEPP 65 code compliance.

In intermittant development at BVN Donovan Hill

##Process##

###3D Studio Max bit###

Each face that you care about needs to be named uniquely so that it can be identified after the fact.

Make a selection set of the faces you are testing, call it `windows`

Make a daylight system. The maxscript is looking for one called `Daylight001` which is the default name.

Set all the materials in the scene to be a standard material in black, except `windows` which should be standard white.

Set your time (etc.) requirements:

```
rootFolder  = "C:\Users\bdoherty\Desktop\AMP_solar\\" --folder to store the images in
hourSubdiv  = 4  --number of images per hour
startTime   = 7  --hour to start at, 24hr clock so it's 0 indexed
endTime     = 19 --hour to end at
startMonth  = 6  --month to start at
endMonth    = 6  --month to end at
outputWidth = 400 --in pixels, the height is set by the aspect ratio of the window
justMakeTheCameras = false --if this is true it won't do the renders.
selectionSetname = "windows" --the name of your selection set.
```

Make sure that you can see the listener (`f11`) then kick off the script. This will take a pretty long time so you'll want something to keep you occupied. It'll only make images if there isn't already an image of this name, so if it crashes then you can just start it again and it'll pick up where it left off.

###Python bit###
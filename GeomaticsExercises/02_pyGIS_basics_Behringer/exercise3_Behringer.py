## -------------EXERCISE 3 --- CARLA BEHRINGER ----------------
# Write a script that finds the station nearest to a given point.

from pyqgis_scripting_ext.core import *
# choosing a point: coordinates of the city where I did my BA 
# (Tübingen, Germany)

tuebi = HPoint(9.05222000 ,48.52266000)


# prepare the stations file
csvPath = "/Users/carlabehringer/iCloud Drive (Archive)/Documents/Documents – Carlas MacBook Air/dokumente/Uni/Master/first_year/Second_semester/Advanced_geomatics/data/class1_0703/stations.txt"

# open file saved as string csvPath in reading mode ('r')
with open(csvPath, 'r') as file:
    lines = file.readlines() # returns a list of lines

# extracting the coordinates,...
 
coordinates=[]
staNameList=[]

for line in lines:
    line=line.strip() #removing empty spaces from beginning and end of lines
    if line.startswith("#") or len(line)==0: #ignoring lines without data
            continue
    #split lines:
    lineSplit = line.split(",")# list of objects for each line
    staName = lineSplit[1]
    staNameList.append(staName.strip())
    lat=lineSplit[3]
    latSplit=lat.split(":")
    lat_deg = int(latSplit[0])
    lat_min = int(latSplit[1])/60
    lat_sec = int(latSplit[2])/3600
    latitude = lat_deg+lat_min+lat_sec
    lon=lineSplit[4]
    lonSplit=lon.split(":")
    lon_deg = int(lonSplit[0])
    lon_min = int(lonSplit[1])/60
    lon_sec = int(lonSplit[2])/3600
    longitude = lon_deg+lon_min+lon_sec
    coords=[longitude,latitude] # ALWAYS THIS WAY ROUND: XAXIS FIRST, YAXIS LATER
    coordinates.append(coords)
multiPoints=HMultiPoint.fromCoords(coordinates)


#------------------------------------------------------------------------------
# calculate the distance of the chosen point to the closest point in my
# multiPoints object
#------------------------------------------------------------------------------

closestDistance=tuebi.distance(multiPoints)
print("distance between stations and point:", closestDistance)

#------------------------------------------------------------------------------
# access the coordinates of the closest point
#------------------------------------------------------------------------------

for coords in coordinates:
    lonpoint=coords[0]
    latpoint=coords[1]
    point=HPoint(lonpoint,latpoint)
    if tuebi.distance(point) == closestDistance:
        coordsPoint = point
        
#------------------------------------------------------------------------------
# access the stations name for the closest point
#------------------------------------------------------------------------------

position=0
for coords in multiPoints.coordinates():
    #coordsPointLon = coords[0]
    for coors in coordsPoint.coordinates():
        if coords[0] == coors[0]:
            staNamePoint = staNameList[position].strip()
    position +=1 

#------------------------------------------------------------------------------
#final print statement:
#------------------------------------------------------------------------------

print("Output for the city of Tübingen:")
print(f"{staNamePoint} -> {coordsPoint}")
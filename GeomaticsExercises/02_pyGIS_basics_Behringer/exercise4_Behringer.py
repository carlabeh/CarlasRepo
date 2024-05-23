## -------------EXERCISE 4 --- CARLA BEHRINGER ----------------
# Write a script that finds the stations within a radius in km of a given
# point using a point-buff ering technique.

from pyqgis_scripting_ext.core import * 

# create the crs helper object and set start and destination
# projection
crsHelper = HCrs()
crsHelper.from_srid(4326)
crsHelper.to_srid(32632) 

# choosing a point: coordinates of my old uni in Tübingen, Germany

tuebi = HPoint(9.05222000 ,48.52266000)

# REPROJECT GEOMETRIES

tuebiTransformed = crsHelper.transform(tuebi) # transform a geometry

print(f"{tuebi} -> {tuebiUTM}'")

# CHOOSE RADIUS: 20 km

tuebiBuffer = tuebiTransformed.buffer(20000)

# prepare the stations file

csvPath = "/Users/carlabehringer/iCloud Drive (Archive)/Documents/Documents – Carlas MacBook Air/dokumente/Uni/Master/first_year/Second_semester/Advanced_geomatics/data/class1_0703/stations.txt"

# open file saved as string csvPath in reading mode ('r')
with open(csvPath, 'r') as file:
    lines = file.readlines() # returns a list of lines

 # extracting the coordinates
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
    # LATITUDE
    lat=lineSplit[3]
    latSplit=lat.split(":")
    lat_deg = int(latSplit[0])
    lat_min = int(latSplit[1])/60
    lat_sec = int(latSplit[2])/3600
    latitude = lat_deg+lat_min+lat_sec
    # LONGITUDE
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
# reproject all the stations and
# access the station names for the points in the buffer
#------------------------------------------------------------------------------

#Transforming the points

pointsTransformed=[]
for point in multiPoints.coordinates():
    pointForReprojection = HPoint(point[0],point[1])
    pointTransformed = crsHelper.transform(pointForReprojection) # reproject stations
    pointsTransformed.append(pointTransformed)
multiPointsTransformed=HMultiPoint(pointsTransformed)

# find the stations in a 20 km Buffer and print the result in the desired format
position=0
for coords in multiPointsTransformed.coordinates():
    transformedPoint=HPoint(coords[0],coords[1])
    stationName = staNameList[position].strip()
    position +=1
    if tuebiBuffer.intersects(transformedPoint) == True:
        radius = tuebiUTM.distance(transformedPoint)/1000
        backTransformedPoint = crsHelper.transform(transformedPoint,inverse=True) #for the printing 
        print(f" {stationName} ({round(radius)} km) -> {backTransformedPoint}")




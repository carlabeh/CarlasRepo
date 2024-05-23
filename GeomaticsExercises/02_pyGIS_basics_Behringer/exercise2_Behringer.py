## -------------EXERCISE 2 --- CARLA BEHRINGER ----------------
# Write a script that plots the positions of the stations in the station
# file.

# While at it, also print out the count of stations per country.

from pyqgis_scripting_ext.core import *

csvPath = "/Users/carlabehringer/iCloud Drive (Archive)/Documents/Documents – Carlas MacBook Air/dokumente/Uni/Master/first_year/Second_semester/Advanced_geomatics/data/class1_0703/stations.txt"

# open file saved as string csvPath in reading mode ('r')
with open(csvPath, 'r') as file:
    lines = file.readlines() # returns a list of lines
    
# count stations per country
stationsCount={}
for line in lines:
    line=line.strip() #removing empty spaces from beginning and end of lines
    if line.startswith("#") or len(line)==0: #ignoring lines without data
        continue
    #extract station ID:
    lineSplit = line.split(",")# list of objects for each line
    country = lineSplit[2]
    counter= stationsCount.get(country, 0) # if key doesn't excist return zero'
    counter += 1
    stationsCount[country] = counter

for key, value in stationsCount.items():
    print(f"{value} of the stations are in {key}.")
    
# extracting the coordinates
coordinates=[]
for line in lines:
    line=line.strip() #removing empty spaces from beginning and end of lines
    if line.startswith("#") or len(line)==0: #ignoring lines without data
            continue
    #split lines:
    lineSplit = line.split(",")# list of objects for each line
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


canvas = HMapCanvas.new()

canvas.set_extent([-180, -90 , 180 ,90])

canvas.add_geometry(multiPoints, "red", 3)

canvas.show()


    
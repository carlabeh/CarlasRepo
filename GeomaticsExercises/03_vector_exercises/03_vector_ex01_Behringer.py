# ---------------------------------------------------------------------------
# ------------- Processing vector data - Exercise 01 ------------------------
# ------------- Carla Behringer ---------------------------------------------
# ---------------------------------------------------------------------------

# 01 - CONVERT THE STATIONS FILE TO GEOPACKAGE
# Parse the stations.txt file and create a vector layer with all the
# columns of the CSV file as attributes. Then save it to geopackage.

from pyqgis_scripting_ext.core import *

# define functions to extract lon + lat from the stations file first

def fromLatString(latString):
    sign = latString[0]
    latDegrees = float(latString[1:3]) # slicing
    latMinutes = float(latString[4:6]) # slicing
    latSeconds = float(latString[7:9]) # slicing
    lat = latDegrees + latMinutes/60 + latSeconds/3600 # abs() converts each number in its positive 
    if sign == '-':
        lat = lat * -1
    return lat
    
def fromLonString(lonString):
    sign = lonString[0]
    lonDegrees = float(lonString[1:4]) 
    lonMinutes = float(lonString[5:7]) 
    lonSeconds = float(lonString[8:10])
    lon = lonDegrees + lonMinutes/60 + lonSeconds/3600
    if sign == '-':
        lon = lon * -1
    return lon

stationsFile = "/Users/carlabehringer/iCloud Drive (Archive)/Documents/Documents – Carlas MacBook Air/dokumente/Uni/Master/first_year/Second_semester/Advanced_geomatics/data/class1_0703/stations.txt"

# open file saved as string csvPath in reading mode ('r')
with open(stationsFile, 'r') as file:
    lines = file.readlines() # returns a list of lines
    
# define the fields for the attribute table
fields = {
    "id": "Integer",
    "name": "String",
    "country" : "String",
    "height" : "Float"
    
}

# create layer
stationsLayer = HVectorLayer.new("stations", "Point", "EPSDG:4326", fields)

# extract data from txt file and add data to the stationsLayer

for line in lines:
    line = line.strip()
    if line.startswith("#") or len(line)==0: #ignoring lines without data
            continue
    lineSplit = line.split(",")
    
    stationID = lineSplit[0].strip()
    
    stationName = lineSplit[1].strip()
    
    countryCN = lineSplit[2].strip()
    
    height = lineSplit[5].strip()
    
    latString = lineSplit[3]
    lonString = lineSplit[4]
    latDec = fromLatString(latString)
    lonDec = fromLonString(lonString)
    
    # add data to the stationsLayer
    stationsLayer.add_feature(HPoint(lonDec,latDec), [stationID, stationName, countryCN, height])
    

# Once we have a memory layer, we can dump it to any supported GIS format:
folder = "/Users/carlabehringer/iCloud Drive (Archive)/Documents/Documents – Carlas MacBook Air/dokumente/Uni/Master/first_year/Second_semester/Advanced_geomatics/scripts/Abgabe/03_vector_exercises"
path = folder + "test.gpkg"
hopeNotError = stationsLayer.dump_to_gpkg(path, overwrite=True) # dump the layer to a geopackage # overwrite false when you want to add a new layer to the gpkg
if(hopeNotError):
    print(hopeNotError) # print out any error, if it happened, hopeNotError is empty when no error


# load the actual dumped layer
testLayer = HVectorLayer.open(path,"stations")
HMap.add_layer(testLayer)
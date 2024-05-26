# ------------- MOCK EXAM -------------------------------
# --- CALUM KITCHING & CARLA BEHRINGER ------------------

from pyqgis_scripting_ext.core import *

# -----------------------------------------------------------------------------
# accessing the Natural earth data set
# -----------------------------------------------------------------------------

folder = "/Users/carlabehringer/iCloud Drive (Archive)/Documents/Documents – Carlas MacBook Air/dokumente/Uni/Master/first_year/Second_semester/Advanced_geomatics"

geopackagePath = folder + "/data/class6_1704/natural_earth_vector.gpkg"
countriesName = "ne_50m_admin_0_countries"


# load the countries layer
countriesLayer = HVectorLayer.open(geopackagePath, countriesName)

# get the features iterator
countriesFeatures = countriesLayer.features()
# get the index of the field "NAME"
nameIndex = countriesLayer.field_index("NAME")
# extract the geometry for France
fieldNames = countriesLayer.field_names

countries = ["Ireland", "France", "Spain"]


for feature in countriesFeatures:
    if feature.attributes[nameIndex] == countries[0]: # attributes are accessed via their index
        geomC1 = feature.geometry # get the geometry
    elif feature.attributes[nameIndex] == countries[1]: # attributes are accessed via their index
        geomC2 = feature.geometry # get the geometry
    elif feature.attributes[nameIndex] == countries[2]: # attributes are accessed via their index
        geomC3 = feature.geometry # get the geometry

# collection out of the three countries
collectionCountries = HGeometryCollection([geomC1, geomC2, geomC3])        

# -----------------------------------------------------------------------------
# accessing the NASA data
# -----------------------------------------------------------------------------

filePath = "/Users/carlabehringer/iCloud Drive (Archive)/Documents/Documents – Carlas MacBook Air/dokumente/Uni/Master/first_year/Second_semester/Advanced_geomatics/mockExam/22yr_T10MN"

#accessing/opening: reading mode (‘r’)
with open(filePath, 'r') as file:
    lines = file.readlines() # returns a list of lines
    

# Part 4: making sure the same script works for the other file by 
# extracting the header index
headerIndex = None

while headerIndex == None:
    for i,line in enumerate(lines):
        if "Jan    Feb    Mar" in line:
            headerIndex = i
            if isinstance(headerIndex, int):
                break

print("Header Index:",headerIndex)

# -----------------------------------------------------------------------------

countriesAvgT =[]
AvgTGrid = []
gridClip = []
color = None

featuresList = [] # to save the features we need: coordinates + average Temperature

for line in lines[headerIndex+1:]: # to start the loop at the line after the header
    line.strip()
    lineSplit = line.split(" ")
    avgT = float(lineSplit[-1].strip()) # access the last column
    lon = int(lineSplit[1])
    lat = int(lineSplit[0])
    # define the polygons as noted down in the comments of the file
    coords = [[lon,lat], [lon+1,lat], [lon+1,lat+1], [lon,lat+1],[lon,lat]] 
    polygon = HPolygon.fromCoords(coords)
    
    # define a color palette
    if avgT < 0:
        color = "green"
        
    elif avgT >= 0 and avgT <= 5:
        color = "darkGreen"
    
    elif avgT > 5  and avgT <= 6.5:
        color = "yellow"
    
    elif avgT > 6.5  and avgT <= 8:
        color = "orange"
    
    elif avgT > 8  and avgT <= 9.5:
        color = "red"
    
    elif avgT > 9.5  and avgT <= 11:
        color = "red"
    
    elif avgT > 11:
        color = "brown"
    
    else:
        color="pink"
    
    # save the features for color scheme and putting them on the canvas
    feature = { 
    "geometry": polygon,
    "temperature": avgT,
    "color": color
    }
    featuresList.append(feature) # results in a list of dictionaries
    
# -----------------------------------------------------------------------------
# put it onto a map
# ----------------------------------------------------------------------------- 

# find out about the projection
crs = countriesLayer.prjcode 
print("Projection: ", crs)

# create the crs helper object and set start and destination
# projection
crsHelper = HCrs()
crsHelper.from_srid(4326) # UTM
crsHelper.to_srid(3857) # OSM

# transform the countries to osm
collectionCountries3857 = crsHelper.transform(collectionCountries)


canvas = HMapCanvas.new()
canvas.show()
osm = HMap.get_osm_layer()
canvas.set_layers([osm])

# put the features on the canvas
for feature in featuresList:
    featureGeom3857 = crsHelper.transform(feature.get("geometry")) # transform
    if collectionCountries3857.intersects(featureGeom3857): # check if it intersects the countries
        clip3857 = collectionCountries3857.intersection(featureGeom3857) # clip it to the countries
        canvas.add_geometry(clip3857, feature.get("color"), 2)
    
canvas.set_extent(collectionCountries3857.bbox()) # bounding box comes in handy
canvas.show()

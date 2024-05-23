# ---------------------------------------------------------------------------
# ------------- Processing vector data - Exercise 03 ------------------------
# ------------- Carla Behringer ---------------------------------------------
# ---------------------------------------------------------------------------

# 03 - CREATE A GPKG WITH THE COUNTRIES CENTROIDS
# Using the Natural Earth datasets, create a new geopackage
# containing the layer of the centroids of the countries.
# Print the names of the countries that do not contain their centroid.

from pyqgis_scripting_ext.core import *

# extract a centroid:
# geometry.centroid()

folder = "/Users/carlabehringer/iCloud Drive (Archive)/Documents/Documents – Carlas MacBook Air/dokumente/Uni/Master/first_year/Second_semester/Advanced_geomatics"

geopackagePath = folder + "/data/class6_1704/natural_earth_vector.gpkg"
countriesName = "ne_50m_admin_0_countries"

# load the countries layer
countriesLayer = HVectorLayer.open(geopackagePath, countriesName)

countriesFeatures = countriesLayer.features()

nameIndex = countriesLayer.field_index("NAME")

# prepare the new Layer with the centroids
fields = {
    "name": "String"
} 

centroidsLayer = HVectorLayer.new("centroids", "Point", "EPSG:4326", fields)

count = 0 
for feature in countriesFeatures: #feature is made of geography + attributes
    name = feature.attributes[nameIndex]
    geometry = feature.geometry
    centroid = geometry.centroid()
    centroidsLayer.add_feature(centroid,[name])
    if not geometry.contains(centroid): # is the centroid contained by the country?
        count+= 1
        print(name)
        
print(count, "countries do not contain their centroid.")


path = folder + "/scripts/Abgabe/03_vector_exercises/centroids.gpkg"
error = centroidsLayer.dump_to_gpkg(path, overwrite=True)
if(error):
    print(error)

# load the actual dumped layer
testLayer = HVectorLayer.open(path,"centroids")
HMap.add_layer(testLayer)
# ---------------------------------------------------------------------------
# ------------- Processing vector data - Exercise 04 ------------------------
# ------------- Carla Behringer ---------------------------------------------
# ---------------------------------------------------------------------------

# 04 - STYLE COUNTRIES BASED ON POPULATION
# Using the Natural Earth datasets, create a nice pdf with a map that
# colors the countries as follows:
# red: population larger than 80000000
# blue: population between 1000000 and 80000000
# green: population smaller than 1000000

from pyqgis_scripting_ext.core import *

# cleanup
HMap.remove_layers_by_name(["population"])


folder = "/Users/carlabehringer/iCloud Drive (Archive)/Documents/Documents – Carlas MacBook Air/dokumente/Uni/Master/first_year/Second_semester/Advanced_geomatics"

geopackagePath = folder + "/data/class6_1704/natural_earth_vector.gpkg"
countriesName = "ne_50m_admin_0_countries"
citiesName = "ne_50m_populated_places"


# load the two layers
countriesLayer = HVectorLayer.open(geopackagePath, countriesName)
countriesFeatures = countriesLayer.features()


#prepare a new Layer with the geometry of the countries and the populations size as attributes
fields = {
    "name": "String",
    "population" : "Integer"
} 
populationLayer = HVectorLayer.new("population", "Polygon", "EPSG:4326", fields)

# find out where the info about the population size is found inside the countriesFeatures

for name, type in countriesLayer.fields.items(): # countriesLayer.fields is a dict, therefore use items
    print("\t", name, "of type", type)
    
# --> POP_EST is the feature we're looking for

nameIndex = countriesLayer.field_index("NAME")
popIndex = countriesLayer.field_index("POP_EST")

for feature in countriesFeatures: #feature is made of geography + attributes
    name = feature.attributes[nameIndex]
    population = feature.attributes[popIndex]
    geometry = feature.geometry
    populationLayer.add_feature(geometry,[name,population])
    

folderPopulation = "/Users/carlabehringer/iCloud Drive (Archive)/Documents/Documents – Carlas MacBook Air/dokumente/Uni/Master/first_year/Second_semester/Advanced_geomatics/scripts/Abgabe/03_vector_exercises/"
path = folderPopulation + "population.gpkg"
error = populationLayer.dump_to_gpkg(path, overwrite=True)
if(error):
    print(error)

# load the actual dumped layer
loadedPopLayer = HVectorLayer.open(path,"population")
HMap.add_layer(loadedPopLayer)

# fieldColor = "if(population> 80000000, HFill('red')), elif(population <= 80000000 and population >= 1000000, HFill('blue')), elif(population< 1000000, HFill('red'))"

# styleProperties = {
# "color": fieldColor,
# "stroke": HStroke('black',0.5)
# }

ranges = [
[0, 1000000],
[1000000, 80000000],
[80000000, 80000000000000000000000]
] 
styles =[
HFill('green'),
HFill('blue'),
HFill('red')
]

loadedPopLayer.set_graduated_style('population', ranges, styles, HStroke('black', 0.1))
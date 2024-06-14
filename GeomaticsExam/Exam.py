# ------------- Geomatics EXAM -------------------------------------------------
# --- KAJA PALASZ, CALUM KITCHING & CARLA BEHRINGER ----------------------------
# ------------- Group 7: Italian mountains higher than 4000 meters -------------

from pyqgis_scripting_ext.core import *

#-------------------------------------------------------------------------------
# First step: run sparql query
#-------------------------------------------------------------------------------

# import the http requests library to get stuff from the internet
import requests
# import the url parsing library to urlencode the query
import urllib.parse

# define the query to launch
endpointUrl = "https://query.wikidata.org/sparql?query=";

# define the query to launch --> putting in our query
query = """
SELECT ?item ?itemLabel ?coord ?elev ?picture
{
?item p:P2044/psn:P2044/wikibase:quantityAmount ?elev ; # normalized height
wdt:P625 ?coord ;
wdt:P17 wd:Q38 ;
wdt:P18 ?picture
FILTER(?elev > 4000)
SERVICE wikibase:label { bd:serviceParam wikibase:language "it" }
}
"""
# URL encode the query string
encoded_query = urllib.parse.quote(query)
# prepare the final url
url = f"{endpointUrl}{encoded_query}&format=json"
# run the query online and get the produced result as a dictionary
r=requests.get(url)
result = r.json()

# print the whole dictionary
#print(result)

# print the header of the dictionary

#print("HEADER:", result.get('head'))

# what can we say about the structure of the dict after looking at the header?
# --> the header is the key and the associated value is a new dictionary
# consisting of vars as a key and the value as a list of ['item', 'itemLabel', 'coord', 'elev', 'picture']

# print the "next line" of the dictionary

print("RESULTS",result.get('results'))

# what can we say about the structure of the dict after looking at the results?
# start with looking at the closing brackets: }}]} 
# --> a dictionary containing a list and the list contains a dictionary within a dictionary
# sounds complicated??
# don't give up!
# let's try to clarify:
# start by looking at the beginning of the dictionary
# 
# --> a dictionary (key1 = "bindings") containing a list (contains all the items)
# and the list contains a dictionary (items as a key) within a dictionary (defines type, value, picture, coord, itemLabel,
# and elev and each of these has values in a form of another dictionary (e.g. 'coord' : {'datatype': 'http://www.opengis.net/ont/geosparql#wktLiteral', 'type': 'literal', 'value': 'Point(7.659722222 45.9775)'} )
# and the coordinates are already an important thing we need for sure for our 
# exercise!

# Now the question is? How to extract these coordinates...?

#-------------------------------------------------------------------------------
# Second step: Create a geopackage based on the result
#-------------------------------------------------------------------------------

#... for the extraction of the coordinates I looked into the Script from the 
# 11.04. (class 5), where we extracted the Meran polygon from the internet
dictNoHeader=result['results']

bindings = dictNoHeader["bindings"]
#check with print statement
print("BINDINGS", bindings)


for i, item in enumerate(bindings): # why enumerate? To print things until a specifc index
    mountain =  item #mountain is item in the dict
    # if i < 2:
    #     print("Mountain", i, mountain)
    for key, value in mountain.items():
        if key == "coord":
            #print(value)
            coordsInfo = value
            for key, value in coordsInfo.items():
                if key == "value":
                    coords = value
                    print(i, coords)                                # WHOOP WHOOP WE HAVE THE COORDINATES!
            





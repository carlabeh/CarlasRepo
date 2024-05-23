# EXERCISE 01 - CREATE AN UTM GRID - CARLA BEHRINGER
# Write a script that generates an UTM grid. Allow the user to change
# the zone extend.

# add canvas

canvas = HMapCanvas.new()


latMin=0 #lat: parallel to equator
lonMin=0 #lon: perpendicular to equator
latMax=180
lonMax=360
canvas.set_extent([lonMin, latMin , lonMax ,latMax]) #x, y bottom left and x,y upper side right


coords = [[lonMin,latMin], [lonMax,latMin], [lonMax,latMax],[lonMin,latMax],[lonMin,latMin]]
polygon = HPolygon.fromCoords(coords)


for i in range(lonMin,lonMax):
    linesMid=HLineString.fromCoords([[lonMin,latMin], [lonMin,latMax]])
    canvas.add_geometry(linesMid,"red",1)
    lonMin+=6

canvas.add_geometry(polygon, "red", 1)

# show results
canvas.show()
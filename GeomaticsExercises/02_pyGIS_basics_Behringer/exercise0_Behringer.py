## -------------EXCERCISE 0 --- CARLA BEHRINGER ----------------
# Write a script that reads geometries from the file
# 02_exe0_geometries.csv and draws them on a new map canvas.

from pyqgis_scripting_ext.core import *

csvPath = "/Users/carlabehringer/iCloud Drive (Archive)/Documents/Documents – Carlas MacBook Air/dokumente/Uni/Master/first_year/Second_semester/Advanced_geomatics/data/class_2803/02_exe0_geometries.csv"

# open file saved as string csvPath in reading mode ('r')
with open(csvPath, 'r') as file:
    lines = file.readlines() # returns a list of lines
# print(lines)

points=[]
geolines=[]
polygons=[]

for line in lines:
    lines=line.strip()
    lineSplit=line.split(";")
    geometry=lineSplit[0]
    coords=lineSplit[1]
    print("This are the coords:",coords)
    num=lineSplit[2]
    #print(lineSplit)
    if geometry=="point":
        coSplit = coords.split(",")
        x=float(coSplit[0])
        y=float(coSplit[1])
        point=HPoint(x,y)
        #print(point)
        points.append(point)
        #print(points)
    elif geometry=="line":
        cSplit=coords.split(" ")
        print("This is cSplit:",cSplit)
        pointList=[]
        for item in cSplit:
            lsplit = item.split(",")
            print(lsplit[0])
            x = float(lsplit[0])
            y = float(lsplit[1])
            pointList.append([x,y])
        geoline = HLineString.fromCoords(pointList)
        geolines.append(geoline)
        print(geolines)
        
    elif lineSplit[0]=="polygon":
        coorSplit=coords.split(" ")
        pointList=[]
        for item in coorSplit:
            lsplit = item.split(",")
            print(lsplit[0])
            x = float(lsplit[0])
            y = float(lsplit[1])
            pointList.append([x,y])
        polygon = HPolygon.fromCoords(pointList)
        polygons.append(polygon)
        print(geolines)
    
canvas = HMapCanvas.new()

for point in points:
    canvas.add_geometry(point, 'black', 15)

for geoline in geolines:
    canvas.add_geometry(geoline, 'green', 3)

for polygon in polygons:
    canvas.add_geometry(polygon, 'orange', 3)

canvas.set_extent([0, 0, 40, 40])
canvas.show()
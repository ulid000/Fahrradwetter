import wradlib as wrl
import warnings
warnings.filterwarnings('ignore')
import numpy as np
import json
from datetime import datetime, date
import os
import pytz
import sys, getopt

def buildGrid(xmin, xmax, ymin, ymax):
    radolan_grid_ll = wrl.georef.get_radolan_grid(900,900, wgs84=True)

    geoJsonGrid = [];

    for x in range(xmin,xmax+1):
        for y in range(ymin,ymax+1):
            gridCell = {}
            gridCell["type"] = "Feature"
            gridProperties = {}
            gridCell["properties"] = gridProperties
            gridProperties["name"] = "RADOLAN_{0}_{1}".format(x,y)                      
            gridGeometry = {}
            gridCell["geometry"] = gridGeometry
            gridGeometry["type"] = "Polygon"
            gridCoordinatesArray = []
            gridGeometry["coordinates"] = gridCoordinatesArray
            gridCoordinates = []
            gridCoordinatesArray.append(gridCoordinates)

            corner1 = []
            corner1.append(radolan_grid_ll[x,y,:][0])
            corner1.append(radolan_grid_ll[x,y,:][1])
            gridCoordinates.append(corner1)

            corner2 = []
            corner2.append(radolan_grid_ll[x,y+1,:][0])
            corner2.append(radolan_grid_ll[x,y+1,:][1])
            gridCoordinates.append(corner2)

            corner3 = []
            corner3.append(radolan_grid_ll[x+1,y+1,:][0])
            corner3.append(radolan_grid_ll[x+1,y+1,:][1])
            gridCoordinates.append(corner3)

            corner4 = []
            corner4.append(radolan_grid_ll[x+1,y,:][0])
            corner4.append(radolan_grid_ll[x+1,y,:][1])
            gridCoordinates.append(corner4)

            corner5 = []
            corner5.append(radolan_grid_ll[x,y,:][0])
            corner5.append(radolan_grid_ll[x,y,:][1])
            gridCoordinates.append(corner5)

            geoJsonGrid.append(gridCell)

    return geoJsonGrid

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return "{0}".format(obj.astimezone(pytz.UTC).isoformat())
    raise TypeError ("Type %s not serializable" % type(obj))

def exportGrid(xmin, xmax, ymin, ymax, outputfile):
    jsonModel = {}
    
    jsonModel["geoJson"] = buildGrid(xmin, xmax, ymin, ymax)
    with open(outputfile, 'w') as fp:
        json.dump(jsonModel, fp, default=json_serial)


def main(argv):
   if(len(sys.argv) != 6):
       print("export-radar-grid.py xmin xmax ymin ymax jsonfile")
       sys.exit(2)

   xmin = int(sys.argv[1])
   ymin = int(sys.argv[2])
   xmax = int(sys.argv[3])
   ymax = int(sys.argv[4])
   outputfile = sys.argv[5]
   print("export-radar-grid.py {} {} {} {} {}".format(xmin, xmax, ymin, ymax, outputfile))
   exportGrid(xmin, xmax, ymin, ymax, outputfile)

if __name__ == "__main__":
   main(sys.argv[1:])
   
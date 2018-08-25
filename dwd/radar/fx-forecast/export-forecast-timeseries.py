import wradlib as wrl
import warnings
warnings.filterwarnings('ignore')
import numpy as np
import json
from datetime import datetime, date
import os
import pytz
import sys, getopt

def readInputFile(sourcefile, forecastSeries, metaSeries):
    filename = sourcefile
    fx_filename = wrl.util.get_wradlib_data_file(filename)

    fxdata, fxattrs = wrl.io.read_RADOLAN_composite(fx_filename)
    fxdata = np.ma.masked_equal(fxdata, -9999) / 2 - 32.5

    forecastSeries.append(fxdata)
    metaSeries.append(fxattrs)

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return "{0}".format(obj.astimezone(pytz.UTC).isoformat())
    raise TypeError ("Type %s not serializable" % type(obj))

def processForecast(fxdirectory, xmin, xmax, ymin, ymax):
    os.environ["WRADLIB_DATA"] = fxdirectory
    forecastSeries = []
    metaSeries = []

    jsonModel = {}

    for root, dirs, files in os.walk(fxdirectory):
        for file in sorted(files):
            if file.endswith("MF002"):
                print(os.path.join(root, file))
                readInputFile(file, forecastSeries, metaSeries)

    metaList = []
    for meta in metaSeries:
        metaList.append(meta['predictiontime'])

    timestamp = metaSeries[0]['datetime']
    jsonModel["timestamp"] = timestamp

    jsonModel["predictiontime"] = metaList
    valuesDict = {}
    jsonModel["values"] = valuesDict

    for x in range(xmin, xmax+1):
        for y in range(ymin, ymax+1):
            predictionList = []
            for prediction in forecastSeries:	    
                value = prediction[x,y]    
                Z = wrl.trafo.idecibel(value)
                R = wrl.zr.z2r(Z, a=200., b=1.6)
                depth = wrl.trafo.r2depth(R, 300)
                # print(type(depth))
                correctedDepth = depth
                if (depth < 0.005):
                    correctedDepth = 0
                predictionList.append(correctedDepth)

            valuesDict["RADOLAN_{0}_{1}".format(x,y)] = predictionList

    for cellName, cellValue in valuesDict.items():
        cellModel = {}
        cellModel['model'] = "RadolanFX"
        cellModel['unit'] = "mm"
        cellModel["name"] = cellName
        cellModel["timestamp"] = timestamp
        cellModel["predictionTime"] = metaList
        cellModel["values"] = cellValue

        with open(cellName + '.json', 'w') as fp:
            from json import encoder
            # encoder.FLOAT_REPR = lambda o: format(o, '.2f')
            json.dump(cellModel, fp, default=json_serial)

def main(argv):
   if(len(sys.argv) != 6):
       print("export-forecast-timesearies.py fxdirectory xmin ymin xmax ymax")
       sys.exit(2)

   fxdirectory = sys.argv[1]
   xmin = int(sys.argv[2])
   ymin = int(sys.argv[3])
   xmax = int(sys.argv[4])
   ymax = int(sys.argv[5])
   print("export-forecast-timeseries.py {} {} {} {} {}".format(fxdirectory, xmin, xmax, ymin, ymax))
   processForecast(fxdirectory, xmin, xmax, ymin, ymax)

if __name__ == "__main__":
   main(sys.argv[1:])
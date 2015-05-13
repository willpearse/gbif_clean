#!/usr/bin/python
# Intersecting data according to buffer

def enumerate_chunk_stream(stream, size):
    chunk = []
    iter = 0
    for i,each in enumerate(stream):
        if (i % size == 0) and i != 0:
            yield iter, chunk
            chunk = []
            iter += 1
        chunk.append(each)
    if len(chunk) > 0:
        yield iter, chunk

#Load params
import sys, yaml, subprocess, os
with (sys.argv[1]) as handle:
    params = yaml.load(handle)

#Setup QGIS
from qgis.core import *
sys.path.append(params["qgis_plugins_path"])
import qgis.utils
from PyQt4.QtCore import QFileInfo
app = QgsApplication([], True)
QgsApplication.setPrefixPath(params["qgis_path"], True)
QgsApplication.initQgis()
import processing #*must* be done here
from processing.core.Processing import Processing
Processing.initialize()
    
#Load buffer
buffer = QgsVectorLayer(params["buffer_file"], "buffer", "ogr")
QgsMapLayerRegistry.instance().addMapLayer(buffer)
    
#Read file and intersect

with open(params["output_file"], "w") as final_handle:
    with open(params["input_file"]) as handle:
        header = handle.next()
        for i, chunk in enumerate_chunk_stream(handle, params["chunk_size"]):
            #Chunk out
            with open(params["temp_file"], "w") as temp_handle:
                temp_handle.write(header)
                [temp_handle.write(each) for each in chunk]
        #Intersect
        layer = QgsVectorLayer("file://"+params["temp_file"]+"?delimiter=%s&xField=%s&yField=%s&crs=epsg:4326" % ("\t", "decimalLongitude", "decimalLatitude"), "curr_chunk", "delimitedtext")
        QgsMapLayerRegistry.instance().addMapLayer(layer)
        processing.runalg("qgis:difference", layer, buffer, params["temp_file"])
        QgsMapLayerRegistry.instance().removeMapLayer(layer.id())
        #Merge (if necessary)
        try:
            os.remove(params["temp_file"]+".csv")
        except OSError:
            pass
        subprocess.call(["ogr2ogr", "-f", "CSV", params["temp_file"]+".csv", params["temp_file"]+".shp", "-lco", "GEOMETRY=AS_WKT"])
        with open(params["temp_file"]+".csv") as temp_handle:
            [final_handle.write(each) for each in temp_handle]

#Cleanup
os.remove(params["temp_file"]+".csv")
QgsApplication.exitQgis()

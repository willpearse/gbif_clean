#!/usr/bin/python
#Preliminary checking and filtering of GBIF data
#Will Pearse - 2015-02-24

#####################
#HEADERS#############
#and#################
#GLOBALS#############
#####################
import argparse, sys
from qgis.core import *
import qgis.utils, processing
QgsApplication.initQgis("/usr", True)

#####################
#MAIN################
#####################
def main():
    #Argument checking
    args = parser.parse_args()
    
    #Setup QGIS buffer layer and temp file
    buffer = QgsVectorLayer("file://"+BUFFER_FILE, "buffer", "delimitedtext")
    QgsMapLayerRegistry.instance().addMapLayer(buffer)
    
    #Chunk through file
    curr_chunk = []
    with open(args.output, "w") as final_handle:
        with open(args.gbif) as handle:
            for i,line in enumerate(handle):
                curr_chunk.append(line)
                header = handle.next()
                if i %% int(args.chunk_size) == 0 & i!=0:
                    #Write out to temp file
                    with open (args.temp_file, "w") as temp_handle:
                        temp_handle.write(header)
                        for each in curr_chunk:
                            temp_handle.write(each)
                            #Perform GIS and and write out                        
                            layer = QgsVectorLayer("file://"+TEMP_FILE+"?delimiter=%s&xField=%s&yField=%s&crs=epsg:4326" % ("\t", "decimalLongitude", "decimalLatitude"), "curr_chunk", "delimitedtext")
                            QgsMapLayerRegistry.instance().addMapLayer(layer)
                            processing.runalg("qgis:intersection", "curr_chunk", "buffer", TEMP_GIS_FILE+"_subset")
                            QgsMapLayerRegistry.instance().removeMapLayer(layer.id())
                            #Append final to final output and cleanup
                    with open(args.temp+"_gis") as temp_handle:
                        temp_handle.next()
                        [final_handle.write(line) for line in temp_handle]
                    curr_chunk = []
    QgsApplication.exitQgis()

#####################
#ARGUMENT HANDLING###
#####################    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="GBIF Intersecting with GIS mask", epilog="http://willpearse.github.com/gbif_clean - Will Pearse (will.pearse@gmail.com)\nRequires QGIS to be correctly setup for scripting - YMMV...")
    parser.add_argument("-gbif", "-i", help="GBIF file (full path)", required=True)
    parser.add_argument("-mask", "-m", help="GIS Shapefile for intersection (full path)", required=True)
    parser.add_argument("-output", "-o", help="Where to write output (full path)", required=True)
    parser.add_argument("-temp", "-t", help="Stem-name for output (full-path)", required=True)
    parser.add_argument("-chunk_size", "-c", help="Chunk size (integer)", default=100000)
    main()

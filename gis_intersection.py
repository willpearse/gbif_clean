#!/usr/bin/python
#Preliminary checking and filtering of GBIF data
#Will Pearse - 2015-02-24

#####################
#HEADERS#############
#and#################
#GLOBALS#############
#####################
import argparse, sys, os
from qgis.core import *
sys.path.append("/usr/share/qgis/python/plugins/")
import qgis.utils
from PyQt4.QtCore import QFileInfo

#####################
#MAIN################
#####################
def main():
    #Argument checking and setup
    args = parser.parse_args()
    #os.environ['DISPLAY']=""
    app = QgsApplication([], True)
    QgsApplication.setPrefixPath("/usr", True)
    QgsApplication.initQgis()
    import processing
    from processing.core.Processing import Processing
    Processing.initialize()
    
    #Setup QGIS and buffer layer
    buffer = QgsVectorLayer(args.mask, "buffer", "ogr")
    #buffer_raster = QgsRasterLayer(args.mask, "buffer_raster")
    #QgsMapLayerRegistry.instance().addMapLayer(buffer_raster)
    #processing.runalg("gdalogr:polygonize", "buffer_raster", False, "buffer_shp")
    #buffer = QgsVectorLayer("buffer_shp", "buffer", "ogr")
    QgsMapLayerRegistry.instance().addMapLayer(buffer)
    
    #Chunk through file
    count = 0
    with open(args.output, "w") as final_handle:
        with open(args.gbif) as handle:
            header = handle.next()
            curr_chunk = [header]
            for i,line in enumerate(handle):
                curr_chunk.append(line)
                if ((i % int(args.chunk_size)) == 0) and (i!=0):
                    #Write out to temp file
                    with open (args.temp+"_subset_"+str(count), "w") as temp_handle:
                        for each in curr_chunk:
                            temp_handle.write(each)
                    #Perform GIS and and write out
                    layer = QgsVectorLayer("file://"+args.temp+"_subset_"+str(count)+"?delimiter=%s&xField=%s&yField=%s&crs=epsg:4326" % ("\t", "decimalLongitude", "decimalLatitude"), "curr_chunk", "delimitedtext")
                    QgsMapLayerRegistry.instance().addMapLayer(layer)
                    processing.runalg("qgis:intersection", layer, buffer, args.temp+"_subset_"+str(count))
                    QgsMapLayerRegistry.instance().removeMapLayer(layer.id())
                    count += 1
                    curr_chunk = [header]
            else:
                #Finish up chunking
                if len(curr_chunk) > 1:
                    with open (args.temp+"_subset_"+str(count), "w") as temp_handle:
                        for each in curr_chunk:
                            temp_handle.write(each)
                    #Perform GIS and and write out
                    layer = QgsVectorLayer("file://"+args.temp+"_subset_"+str(count)+"?delimiter=%s&xField=%s&yField=%s&crs=epsg:4326" % ("\t", "decimalLongitude", "decimalLatitude"), "curr_chunk", "delimitedtext")
                    QgsMapLayerRegistry.instance().addMapLayer(layer)
                    processing.runalg("qgis:intersection", layer, buffer, args.temp+"_subset_"+str(count))
                #Merge layers
                print "merging..."
    
    print "finished"
    QgsApplication.exitQgis()


#####################
#ARGUMENT HANDLING###
#####################    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="GBIF Intersecting with GIS mask", epilog="http://willpearse.github.com/gbif_clean - Will Pearse (will.pearse@gmail.com)\nRequires QGIS to be correctly setup for scripting - YMMV...")
    parser.add_argument("-gbif", "-i", help="GBIF file (full path)", required=True)
    parser.add_argument("-mask", "-m", help="Raster for intersection (full path)", required=True)
    parser.add_argument("-output", "-o", help="Where to write output (full path)", required=True)
    parser.add_argument("-temp", "-t", help="Stem-name for output (full-path)", required=True)
    parser.add_argument("-chunk_size", "-c", help="Chunk size (integer)", default=100000)
    main()

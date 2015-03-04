GBIF Cleaning
=============
Will Pearse

##Overview
A set of GBIF cleaning scripts that I find useful. All of them can be run from the command line, and all assume that you are running my computer (Ubuntu 14.04 LTS) with QGIS installed (see below for note). Your Mileage May Vary; these scripts should on your (Mac/Linux) system, and I will try and help you if you get stuck, but you pays your money and your makes your choice :D

##Components
* _text_stripping.py_
  Filters GBIF records according to fields, and filters out unwanted fields from the dump. Filtering is more important than you might think; the filesizes will become much (~1/10-->1/20th) smaller, and latter calculations much quicker, once it's filtered. The GLOBAL VARIABLES that determine the filtering are at the top of the script.
* _gis_intersction.py_
  Outputs the intersection of given (optionally filtered) GBIF records and polygon (tested only with shapefile). Good for finding records on certain continents, habitat types, etc.
* _filter_species.py_
  Produces counts of species' occurrences in the input, and (when ````-threshold```` is supplied) removes any species below that threshold. Beware synonymy!

##QGIS
Several of these scripts assume you have QGIS installed; these scripts are prefixed by 'gis'. At the start of such scripts is a line like
````python
QgsApplication.initQgis("/usr/share/qgis", True)
````
...this may need altering depending on where your QGIS is installed (see Running Custom Applications; http://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/intro.html).

##License
As stated in LICENSE file, MIT. Might be nice if you bought me a beer though :D
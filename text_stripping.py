#!/usr/bin/python
#Preliminary checking and filtering of GBIF data
import sys, yaml

#####################
#FUNCTIONS###########
#####################
#Define mask and header lookup
def define_mask(header, fields={"hasGeospatialIssues":"FALSE", "hasCoordinates":"TRUE", "basisOfRecord":"SPECIMEN"}):
    header = header.strip().split("\t")
    mask = {key:value for (key,value) in zip([header.index(x) for x in fields], fields.values())}
    issue_column = header.index("issue")
    return mask, issue_column

#Mask and lookup functions
def mask_data(line, mask):
    line = line.strip().split("\t")
    for key,value in mask.iteritems():
        if line[key] != value:
            return False
    return True

def trim_data(line, header, fields=['gbifID', 'decimalLatitude', 'decimalLongitude', 'species']):
    line = line.strip().split("\t")
    header = header.strip().split("\t")
    return [line[header.index(x)] for x in fields]

def issue_mask(line, mask, issue_column):
    line = line.strip().split("\t")
    for each in mask:
        if line[issue_column] == each:
            return False
    return True


#####################
#MAIN################
#####################
with open(sys.argv[1]) as handle:
    params = yaml.load(handle)
#Load file
with open(params["output_file"], "w") as write_handle:
    with open(params["input_file"]) as handle:
        #Setup mask and header
        header = handle.next()
        mask, issue_column = define_mask(header, params["mask"])
        write_handle.write("\t".join(params["output_fields"])+"\n")
        #Do work
        for line in handle:
            if mask_data(line, mask):
                write_handle.write("\t".join(trim_data(line, header, params["output_fields"]))+"\n")
                

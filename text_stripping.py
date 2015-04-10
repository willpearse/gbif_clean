#!/usr/bin/python
#Preliminary checking and filtering of GBIF data
#Will Pearse - 2015-02-24

#####################
#HEADERS#############
#and#################
#GLOBALS#############
#####################
import argparse, sys, collections
MASK = {"hasGeospatialIssues":"false", "hasCoordinate":"true", "basisOfRecord":"OBSERVATION"}
FIELDS = ['gbifID', 'decimalLatitude', 'decimalLongitude', 'species']

#####################
#FUNCTIONS###########
#####################
#Define mask and header lookup
def define_mask(header, fields={"hasGeospatialIssues":"FALSE", "hasCoordinates":"TRUE", "basisOfRecord":"OBSERVATION"}):
    header = header.strip().split("\t")
    mask = {key:value for (key,value) in zip([header.index(x) for x in fields], fields.values())}
    return mask
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
   
#####################
#MAIN################
#####################
def main():
    #Argument checking
    args = parser.parse_args()

    #Setup for duplicate-check

    
    #Load file
    with open(args.output, "w") as write_handle:
        with open(args.input) as handle:
            #Setup mask and header
            header = handle.next()
            mask = define_mask(header, MASK)
            write_handle.write("\t".join(FIELDS)+"\n")
            #Do work
            # - separately if looking for duplicates as it's slower
            if args.rm_dups:
                counter = collections.Counter()
                count_index = header.split("\t").index("occurrence_id")
                for line in handle:
                    curr_id = line.split("\t")[count_index]
                    counter[curr_id] += 1
                    if mask_data(line, mask) and counter[curr_id]<=1:
                        write_handle.write("\t".join(trim_data(line, header, FIELDS))+"\n")
            else:
                #No duplicate check
                for line in handle:
                    if mask_data(line, mask):
                        write_handle.write("\t".join(trim_data(line, header, FIELDS))+"\n")



#####################
#ARGUMENT HANDLING###
#####################    
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="GBIF Preliminary Cleaning", epilog="http://willpearse.github.com/gbif_clean - Will Pearse (will.pearse@gmail.com)")
	parser.add_argument("-input", "-i", help="GBIF dump file (full path)", required=True)
        parser.add_argument("-output", "-o", help="Where to write output (full path)", required=True)
        parser.add_argument("--rm_dups", "-d", help="If given, remove duplicates according to occurrence_id", action="store_true")
	main()

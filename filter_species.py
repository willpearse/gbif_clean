#!/usr/bin/python
#Filtering species on the basis of occurrence
#Will Pearse - 2015-03-04

#####################
#HEADERS#############
#and#################
#GLOBALS#############
#####################
import argparse, sys, collections

#####################
#MAIN################
#####################
def main():
    #Argument checking
    args = parser.parse_args()

    #Creat occurrence counts
    counts = collections.Counter()
    with open(args.input) as handle:
        header = handle.next().strip().split("\t")
        sp_index = header.index("species")
        for line in handle:
            line = line.split("\t")
            counts[line[sp_index]] += 1

    #Write out counts and exit if asked
    if not args.threshold:
        with open(args.output, "w") as handle:
            handle.write("species\tcount\n")
            for sp,count in counts.iteritems():
                handle.write(sp+"\t"+str(count)+"\n")
        sys.exit()
    
    #Loop over and keep values greater than cut-off
    with open(args.output, "w") as write_handle:
        with open(args.input) as handle:
            write_handle.write(handle.next())
            for line in handle:
                tmp = line.strip().split("\t")
                if counts[tmp[sp_index]] >= int(args.threshold):
                    write_handle.write(line)
    
#####################
#ARGUMENT HANDLING###
#####################    
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="GBIF Preliminary Cleaning", epilog="http://willpearse.github.com/gbif_clean - Will Pearse (will.pearse@gmail.com)")
	parser.add_argument("-input", "-i", help="GBIF dump file (full path)", required=True)
        parser.add_argument("-output", "-o", help="Where to write output (full path)", required=True)
        parser.add_argument("-threshold", "-t", help="Thresold occurrence for keeping values (supply to generate trimmed list, else species-occurrence table is output)")
	main()

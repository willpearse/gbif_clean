#!/usr/bin/python
#Merging taxonomies

import sys, codecs, datetime, yaml
from synonymize import read_names
from fuzzy_match import fuzzy_match_name_list
#...assumes taxon-names-utils exists somewhere

#####################
#MAIN################
#####################
#...note that entries missing species complicates handling lines
with open(sys.argv[1]) as handle:
    params = yaml.load(handle)

#Get species lists
species = set()
with open(params["input_gbif"]) as handle:
    header = handle.next().strip().split("\t")
    col = header.index("species")
    [species.add(unicode(line.split("\t")[col].strip(), "utf-8")) for line in handle]
match_names = read_names(codecs.open(params["input_match"], "r", "utf-8"))

#Write lookup output; create internal copy
with codecs.open(params["output_lookup"], "w", "utf-8") as handle:
    lookup_table = fuzzy_match_name_list(species, match_names, handle)

#Rename GBIF input
with open(params["input_gbif"]) as read_handle:
    with open(params["output_gbif"], "w") as write_handle:
        header = read_handle.next()
        col = header.strip().split("\t").index("species")
        write_handle.write(header)
        for line in read_handle:
            line = line.split("\t")
            sp = line[col].strip()
            if sp in lookup_table.keys():
                line[col] = lookup_table[sp]
                write_handle.write("\t".join(line) + "\n")

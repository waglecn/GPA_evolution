#!/usr/bin/env python
import sys
import ete3

incoming_tree = sys.argv[1]

gtree = ete3.Tree(incoming_tree, format=1)
print(str(gtree))

species_dict = {}
for n in gtree:
    name_parts = n.name.split('_')
    species = name_parts[0]
    if species not in species_dict:
        species_dict[species] = 0
    gene_num = species_dict[species]
    species_dict[species] += 1
    n.name = '{0}_{1}'.format(species, gene_num)

print(str(gtree))
gtree.write(outfile='gtree.renamed.tree')

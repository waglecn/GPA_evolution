#!/usr/bin/env python
import sys
import ete3

incoming_tree = sys.argv[1]
outgoing_tree = '.'.join(incoming_tree.split('.')[:-1]) + '.renamed.tree'
print('read: {0}'.format(incoming_tree))
t = ete3.Tree(incoming_tree, format=1)

for s in t:
    print(s.name)
    s.name = s.name.split('_')[0]

t.write(outfile=outgoing_tree)
print('wrote: {0}'.format(outgoing_tree))

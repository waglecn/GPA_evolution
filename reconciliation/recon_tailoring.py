#!/usr/bin/env python3
import os
import sys
import subprocess

stree_file = "/home/nick/Downloads/v3/9_reconciliation/stree03-WAGurcBD-200m-combined.renamed.tree"
try:
    stree_file = sys.argv[1]
    assert os.path.exists(stree_file)
except IndexError as e:
    exit('stree file not specified')
except AssertionError as e:
    exit('stree file does not exist')

gene_list = [
    "tree01_MbtH.tree",
    "tree02_hal.tree",
    "tree03_deAc.tree",
    "tree04_hydAcyltf.tree",
    "tree05_hydAcyltfII.tree",
    "tree06_P450.tree",
    "tree07_gtfI.tree",
    "tree08_gtfII.tree",
    "tree09_mbgtfI.tree",
    "tree10_mbgtfII.tree",
    "tree11_stf.tree",
    "tree12_mtfI.tree",
    "tree13_mtfII.tree",
    "tree14_mtfIII.tree",
    "tree15_mtfIV.tree",
    "tree16_omtfI.tree",
    "tree17_omtfII.tree",
    "tree18_omtfIII.tree",
    "tree19_Nmtf.tree"
]

schemes = [
    'A00', 'B00', 'A10', 'B10', 'C01', 'C03',
]
try:
    schemes = sys.argv[2:]
    assert len(schemes) > 0
except Exception as e:
    print('no/incorrect scheme specified, using default C03 scheme')
    schemes = ['C03']

for g in gene_list:
    for s in schemes:
        print('==== {0} ===='.format(s))
        # set costs
        costs = ''
        if s[0] == 'A':
            costs = ["dupli.cost=1", "HGT.cost=1", "loss.cost=1"]
        elif s[0] == 'B':
            costs = ["dupli.cost=1", "HGT.cost=3", "loss.cost=1"]

        # allow to/from dead?
        dead = "compute.TD=false"
        if s[1] == '1':
            dead = "compute.TD=true"

        # pareto mod?

        if s[2] == '0':
            pareto = ["pareto.mod=0"]
        elif s[2] == '1':
            pareto = [
                "pareto.mod=1",
                "nD=0.4",
                "nL=0.4",
                "nDL=0.4"
            ]
        elif s[2] == '3':
            pareto = [
                "pareto.mod=3",
                "suboptimal.epsilon=1",
                "real.epsilon=1"
            ]

        # prefix
        prefix = '{0}_{1}'.format(g.split('.')[0], s)

        cmd = [
            "ecceTERA_linux64",
            "species.file=" + stree_file,
            # "species.file=/media/C/Downloads/Work-Other/v3/9_reconciliation/stree02-WAGurcBD-100m.renamed.tree",
            "gene.file=" + g,
            "resolve.trees=1",
            "print.newick=1",
            "verbose=true",
            "print.info=true",
            "print.reconciliations=1",
            "output.prefix=" + prefix,
        ]
        cmd += costs
        cmd += [dead]
        cmd += pareto

        print(cmd)
        output = subprocess.check_output(cmd)
        print(output.decode('utf-8'))


# Example parameters for strategy s3:
# bin/ecceTERA species.file=tests/Stree.tree gene.file=tests/HBG284008_1.gtrees
# compute.TD=0 pareto.mod=1 nD=0.4 nL=0.4 nDL=0.4
# Example parameters for strategy s4:
# bin/ecceTERA species.file=tests/Stree.tree gene.file=tests/HBG284008_1.gtrees
# com­pute.TD=0 pareto.mod=2 suboptimal.epsilon=1 real.epsilon=1
# Example parameters for strategy s5:
# bin/ecceTERA species.file=tests/Stree.tree gene.file=tests/HBG284008_1.gtrees
# com­pute.TD=0 pareto.mod=3 suboptimal.epsilon=1 real.epsilon=1

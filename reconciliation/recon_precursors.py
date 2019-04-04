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
    "tree01_DAHPS1.tree",
    "tree02_DAHPS2.tree",
    "tree03_CM1.tree",
    "tree04_CM2.tree",
    "tree05_pdh.tree",
    "tree06_HmaS.tree",
    "tree07_Hmo.tree",
    "tree08_HpgT.tree",
    "tree09_DpgA.tree",
    "tree10_DpgB.tree",
    "tree11_DpgC.tree",
    "tree12_DpgD.tree",
    "tree13_OxyD.tree",
    "tree14_Bhp.tree",
    "tree15_BpsD.tree",
    "tree16_EvaA.tree",
    "tree17_EvaB.tree",
    "tree18_EvaC.tree",
    "tree19_EvaD.tree",
    "tree20_KR.tree",
    "tree21_G1PTtf.tree",
    "tree22_bOHase.tree"
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
        if s[1] == '0':
            dead = "compute.TD=false"
        elif s[1] == '1':
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

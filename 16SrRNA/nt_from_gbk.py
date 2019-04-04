#!/usr/bin/env python
import os
import subprocess
from Bio import SeqIO
from progress import bar

f_dir = '../input_genome_sequences'
file_list = os.listdir(f_dir)
file_list = [f for f in file_list if f.endswith('.gbk')]
pbar = bar.Bar('files ', max=len(file_list))
for f in file_list:
    pbar.next()
    records = SeqIO.parse(os.path.join(f_dir, f), 'gb')
    new_file_name = f + '.fn'
    outh = open(new_file_name, 'w')
    for r in records:
        outh.write(r.format('fasta'))
    outh.close()
    rRNA_output = f + '.rnammer.bac.fasta'
    with open(rRNA_output, 'w') as file_handle:
        pass
    cmd = [
        'perl',
        '/home/nick/Downloads/rnammer-1.2/rnammer',
        '-S', 'bac',
        '-multi',
        '-m', 'lsu,ssu,tsu'
        '-f', rRNA_output,
        new_file_name
    ]
    result = subprocess.check_output(cmd)

pbar.finish()

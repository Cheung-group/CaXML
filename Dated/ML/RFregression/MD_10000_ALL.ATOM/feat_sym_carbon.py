#!/usr/bin/env python
# coding: utf-8

from Bio.PDB import *
from biopandas.mol2 import PandasMol2
import glob
import math
import numpy as np
import sys

# Data file
snapshot = sys.argv[1]

pmol = PandasMol2().read_mol2(snapshot)
pmol.df[pmol.df['atom_type'] == 'c3']

# Features
atoms = [x for x in structure.get_atoms()]
for i in atoms:
    if i.parent.get_resname() in ['CA ', ' CA']:
        calAtom = i
atomindex = calAtom.serial_number - 1


ele = dict()
ele['C'] = []
ele['N'] = []
ele['O'] = []
ele['H'] = []

for i in atoms:
    ele[i.element].append(i.serial_number-1)

feat = feature(structure)
for num in feat:
    print("%f " % num, end = '')
#print("------------- %s finished----------------" %struct)
print("\n", end = '')

#from Bio import PDB
from Bio.PDB import *
import glob
CaMKII = glob.glob("input.loop3/CaMKII_loop3_*.pdb")
holoCaM = glob.glob("input.loop3/holoCaM_loop3_*.pdb")
Ng=glob.glob("input.loop3/Ng-*_loop3_*.pdb")
loop3Size = 176

files = glob.glob("output.loop3/*.txt")
charge = dict()
for chgFile in files:
    prot = chgFile.split('/')[1].split('.')[1]
    with open(chgFile,"r") as file1:
        for line in file1:
            line = line.strip().split()
            charge[(prot,line[0])] = line[1]

output = open("distData.txt", 'w+')


def count(gen):
    return sum(1 for _ in gen.get_atoms())

parser = PDBParser()
structure = parser.get_structure('loop3', 'input.loop3/CaMKII_loop3_0.0.pdb')
if count(structure) != loop3Size:
    print("Error in atom number!\n")
    raise SystemExit(1)

for i in structure.get_atoms():
    if i.parent.get_resname() == ' CA':
        calAtom = i

for i in structure.get_residues():
    resid = i.get_id()[1]
    if resid != 92 and resid != 105 and i.get_resname() != ' CA':
        for j in i.get_atoms():
            if j.mass > 1.1:
                par = j.name + '-' + str(resid) + '-' + 'Ca'
                output.write("%s," % par)
output.write("Cachg\n")

import numpy as np
# Print the coordinates
for struct in CaMKII + holoCaM + Ng:
    prot = struct.split('/')[1].split('_')[0]
    index = struct.split('/')[1].split("_")[2].split('.pdb')[0]
    idf = (prot, index)
    if idf in charge:
        cach =  charge[(prot,index)]
        structure = parser.get_structure(struct.split('/')[1],struct)
        if count(structure) != loop3Size:
            print("Error in atom number!\n")
            raise SystemExit(1)

        for i in structure.get_atoms():
            if i.parent.get_resname() == ' CA':
                calAtom = i

        for i in structure.get_residues():
            resid = i.get_id()[1]
            if resid != 92 and resid != 105 and i.get_resname() != ' CA':
                for j in i.get_atoms():
                    if j.mass > 1.1:
                        val = np.linalg.norm(j.coord - calAtom.coord)
                        output.write("%s," % val)
        output.write("%s\n" % cach)

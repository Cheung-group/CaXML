#!/usr/bin/env python
# coding: utf-8

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
            charge[(prot,line[0])]=line[1]

output = open("TestData.txt", 'w+')

def count(gen):
    return sum(1 for _ in gen.get_atoms())

parser = PDBParser()
structure = parser.get_structure('loop3', 'input.loop3/CaMKII_loop3_0.0.pdb')
if count(structure) != loop3Size:
    print("Error in atom number!\n")
    raise SystemExit(1)

# Print the header
for i in structure.get_atoms():
    par=i.name+'-'+str(i.full_id[3][1])
    output.write("%s," % par)
    for j in range(3):
        par = i.name + '-' + str(i.full_id[3][1]) + chr(j+88)
        val = i.get_coord()[j]
        output.write("%s," % par)
output.write("Cachg\n")

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
            output.write("%f," % i.mass)
            for j in range(3):
                par = i.name + '-' + str(i.full_id[3][1]) + chr(j+88)
                val = i.get_coord()[j]
                output.write("%s," % val)
        output.write("%s\n" % cach)


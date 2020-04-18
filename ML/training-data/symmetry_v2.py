#!/usr/bin/env python
# coding: utf-8

from Bio.PDB import *
import glob
import math
import numpy as np

loop3Size = 176
# Data files
CaMKII = glob.glob("input.loop3/CaMKII_loop3_*.pdb")
holoCaM = glob.glob("input.loop3/holoCaM_loop3_*.pdb")
Ng = glob.glob("input.loop3/Ng-*_loop3_*.pdb")

# Extract the charges
chgFiles = glob.glob("output.loop3/*.txt")
charge = dict()

for chgFile in chgFiles:
    prot = chgFile.split('/')[1].split('.')[1]
    with open(chgFile,"r") as file1:
        for line in file1:
            line = line.strip().split()
            charge[(prot,line[0])] = line[1]

def count(gen):
    """
    Count number of atoms
    """

    return sum(1 for _ in gen.get_atoms())

def cutoff(r_ij, r_cut):
    """
    Radial Cutoff function
    """

    if r_ij > r_cut:
        return 0
    else:
        return 0.5*(math.cos(math.pi*r_ij/r_cut)+1)


def Rad(r_min, r_max, r_inc):
    """
    Radial distribution function to a selected atom
    with respect to r_cut ranging from r_min to r_max at increment r_inc
    tau controls how fast the curve goes to 0 (r_cut)
    Here we use very small tau.
    """
    feat = []
    tau = 0.0001
    at = atoms[atomindex]
    for element in ele:
        atomlist = ele[element]
        for r_cut in np.arange(r_min,r_max+0.5*r_inc,r_inc):
            #print("rcut is %f" %r_cut)
            g_rad = 0
            for i in atomlist:
                a = atoms[i]
                r_ij = np.linalg.norm(a.coord - at.coord)
                #print("rij is %f" %r_ij)
                g_rad += np.exp(-tau*r_ij*r_ij)*cutoff(r_ij, r_cut)
            feat.append(g_rad)
    return feat

def Ang(r_cut):
    """
    Angular distribution function to a selected atom.
    n controls sensitivity in angle.
    """
    feat = []
    tau = 0.0001
    n = 0.5
    at = atoms[atomindex]
    for element in ele:
        atomlist = ele[element]
        for element2 in ele:
            atomlist2 = ele[element2]
            g_ang = 0
            for k in atomlist:
                for j in atomlist2:
                    ak = atoms[k]
                    aj = atoms[j]
                    r_ij = np.linalg.norm(at.coord - aj.coord)
                    r_ik = np.linalg.norm(at.coord - ak.coord)
                    r_kj = np.linalg.norm(ak.coord - ak.coord)

                    cos_ikj = np.inner((at.coord - aj.coord), (at.coord - ak.coord))/(r_ij*r_ik)
                    #print("cosine angle is %f " % cos_ikj)
                    f1 = np.power(round((0.5-cos_ikj*0.5), 6),n)
                    f2 = np.exp(-tau*(r_ij*r_ij+r_ik*r_ik+r_kj*r_kj))
                    f3 = cutoff(r_ij, r_cut)*cutoff(r_ik, r_cut)*cutoff(r_kj, r_cut)
                    #print("%f %f %f" %(f1, f2, f3))
                    g_ang += 2*f1*f2*f3
            feat.append(g_ang)
    return feat

def feature(struct):
    """
    Feature vector has 80 elements:
    Matrix Rad 0-54: radial (0-10: H; 11-21: C; 22-32: O; 33-43: N; 44-54: S)
    Matrix Ang 55-79: angular (H-H H-C H-O H-N H-S; C-H C-C C-O C-N C-S;)
    """
    global atoms
    atoms = [ x for x in struct.get_atoms()]

    return Rad(1.0, 6.0, 0.5) + Ang(3.0)

# Print the symmetry functions
output = open("sym.txt", 'w+')
cnt = 0
parser = PDBParser()

# Features
# Run only once
structure = parser.get_structure('loop3', 'input.loop3/CaMKII_loop3_0.0.pdb')
atoms = [x for x in structure.get_atoms()]
for i in atoms:
    if i.parent.get_resname() == ' CA':
        calAtom = i
atomindex = calAtom.serial_number - 1

residues = [i for i in structure.get_residues()]

ele = dict()
ele['C'] = []
ele['N'] = []
ele['OW'] = []
ele['OCoor'] = []
ele['O'] = []
ele['H'] = []

for i in atoms:
    if i.element == 'O':
        if i.parent is residues[7] and i.get_name() == 'O':
            ele['OCoor'].append(i.serial_number-1)
        elif i.get_name() == 'OW':
            ele['OW'].append(i.serial_number-1)
        else:
            ele[i.element].append(i.serial_number-1)
    if i.parent in [residues[1], residues[3], residues[5], residues[12]]:
        if i.get_name() in ['OE1','OE2','OD1','OD2']:
            ele['OCoor'].append(i.serial_number-1)
    if i.element in ['C', 'N', 'H']:
        if not i is calAtom:
            ele[i.element].append(i.serial_number-1)

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

        feat = feature(structure)
        for num in feat:
            output.write("%f," % num)
        output.write("%s\n" % cach)

    print("------------- %s finished----------------" %struct)

#print the header
r_min=1.0
r_max=6.0
r_inc=0.5
for element in ele:
    for cut in np.arange(r_min,r_max+0.5*r_inc,r_inc):
        print(element+str(cut), end=",")
for element in ele:
    for element2 in ele:
        print(element+":"+element2, end=",")
print("Cachg")

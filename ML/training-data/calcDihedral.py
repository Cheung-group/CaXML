from Bio.PDB import *
import numpy as np
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

# chain is a list of residues
chain=structure.child_list[0].child_list[0].child_list
calRes = chain[14]
WatRes = chain[15]
loopRes = chain[1:13]

for res in loopRes:
    resid = res.get_id()[1]
    for atom in res:
            if atom.mass > 1.1:
                par = atom.name + '-' + str(resid) + '-' + 'Ca'
                output.write("%s," % par)
output.write("Loop-Ca-OW,Loop-Ca-OW-HW,")
output.write("Cachg\n")

# Print the angle COM_loop-Ca-OW, dihedral angle OW-HW-Ca-COM_loop
for struct in CaMKII + holoCaM + Ng:
    prot = struct.split('/')[1].split('_')[0]
    index = struct.split('/')[1].split("_")[2].split('.pdb')[0]
    idf = (prot, index)
    if idf in charge:
        cach =  charge[idf]

        COM = np.zeros([3])
        mass = 0

        structure = parser.get_structure(struct.split('/')[1],struct)
        if count(structure) != loop3Size:
            print("Error in atom number!\n")
            raise SystemExit(1)

        chain=structure.child_list[0].child_list[0].child_list
        calRes = chain[14]
        calAtom = calRes.child_list[0]
        WatRes = chain[15]
        OWAtom = WatRes.child_list[0]
        HWAtom = WatRes.child_list[1]
        loopRes = chain[1:13]

        for res in loopRes:
            resid = res.get_id()[1]
            for atom in res:
                    if atom.mass > 1.1:
                        val = 1.0/np.linalg.norm(atom.coord - calAtom.coord)
                        output.write("%f," % val)
                        COM = COM + atom.coord*atom.mass
                        mass = mass + atom.mass

        angle = calc_angle(Vector(COM/mass),Vector(calAtom.coord),Vector(OWAtom.coord))
        output.write("%f," % angle)

        diangle = calc_dihedral(Vector(COM/mass),Vector(calAtom.coord),Vector(OWAtom.coord),Vector(HWAtom.coord))
        output.write("%f," % diangle)

        output.write("%s\n" % cach)

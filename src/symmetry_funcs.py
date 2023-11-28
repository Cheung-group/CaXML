import numpy as np
from ase.io import read
from dscribe.descriptors import ACSF
from pathlib import Path


# Atomic number to element symbol
aN={1:'H',6:'C',7:'N',8:'O',20:'Ca'}
elements = ['H','C','N','O','Ca']

class Structure:
    """
    The class takes the pdb file and extract the symmetry functions.
    
    Parameters
    ----------
    pdb_path : Path
        The path to the pdb file.
    """
    
    def __init__(self, pdb_path):
        self.pdb_path = Path(pdb_path) if isinstance(pdb_path, str) else pdb_path
        self.name = pdb_path.stem
        # self.feat_atom = dict()
        
    def calc_sym(self):
        '''
        The function takes the structure file and compute the 
        symmetry function for each atom
        output: a list of symmetry functions for each atom. 
                Length of the list = number of atoms
            UPDATE: remove water molecules.
        ''' 


        # Read the pdb file using ase.io.read
        # PZhang: For some reason (format of pdb?), some atom symbols are not correct if not provided.
        # example: out_5cpv.pdb_match_4.pdb
        # Cd, Ce, Og, are not recognized by ASE as C, C, and O.
        # Atoms(symbols='C77Ca29Cd15Ce8N32O41Og4', pbc=False, atomtypes=..., bfactor=..., occupancy=..., residuenames=..., residuenumbers=...)
        # To avoid this problem, we provide the element symbols in columns 77 and 78 of the pdb file.
        ## From the ase code:
            # if line.startswith('ATOM') or line.startswith('HETATM'):
            # Atom name is arbitrary and does not necessarily
            # contain the element symbol.  The specification
            # requires the element symbol to be in columns 77+78.

        structure = read(self.pdb_path)
        feat_lst=[]
        num=structure.get_global_number_of_atoms()
        atomPos = [x for x in range(0,num)]

        #for r_cut in [x/4. for x in range(4,13,1)]:
         
        # Setting up the ACSF descriptor
        for r_cut in [4.]:
            acsf = ACSF(
                species=elements,
                r_cut=r_cut,
                g2_params=[[0.0001,0]],
            )
            feat_lst.append(acsf.create(structure, centers=atomPos, n_jobs=4))

        acsf_ang = ACSF(
            species=elements,
            r_cut=6.0,
            g4_params=[[0.0001,0.5,-1]],
        )
        feat_lst.append(acsf_ang.create(structure, centers=atomPos, n_jobs=4))

        feat = np.hstack(tuple(feat_lst))
        np.savetxt(f'sym_{self.name}.csv', feat, delimiter=',')
        
        # # Skip water here
        # # Skip to the last water x 3 rows
        # skip_water = -3 * self.water
        # # If there is no water, skip none (-1)
        # if skip_water == 0:
        #     skip_water = None
        # #print("skip water atoms",skip_water)
        # #print(dat.shape)
        # #print(dat[:skip_water,:].shape)
        # for i in dat[:skip_water,:]:
        #     ikey = aN[int(i[-2])]
        #     if ikey in self.feat_atom:
        #         self.feat_atom[ikey] = np.vstack((self.feat_atom[ikey],i))
        #     else:
        #         #print(ikey,"is not in the dictionary, adding ...")
        #         self.feat_atom[ikey] = i

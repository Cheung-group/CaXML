import numpy as np
import pandas as pd
from ase.io import read
from dscribe.descriptors import ACSF
from pathlib import Path


# Atomic number to element symbol
aN={1:'H', 6:'C', 7:'N', 8:'O', 16:'S', 20:'Ca'}
#elements = ['H','C','N','O','Ca']
elements = ['C', 'N', 'O', 'S', 'Ca']

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
        self.name = self.pdb_path.stem
        self.feat_atom = {}
        
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

        # Skip hydrogen atoms here
        structure = structure[structure.get_atomic_numbers() > 1]
        feat_lst = []

        # Get the position of the calcium atom
        try:
            atomPos = np.where(structure.get_array('residuenames') == ' CA ')[0]
        except:
            raise ValueError(f'No calcium atom recognized in {self.name}. Make sure the calcium ion residuename is " CA "')

         
        # Setting up the ACSF descriptor
        for r_cut in [2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0]:
            acsf = ACSF(
                species=elements,
                r_cut=r_cut,
                g2_params=[[0.0001, 0]],
            )

            # skipping g1 here
            feat_lst.append(acsf.create(structure, centers=atomPos, n_jobs=4)[:, 5:])
            # 5 x 8 = 40 features 

        for r_cut in [3.0, 6.0]:
            acsf_ang = ACSF(
                species=elements,
                r_cut=r_cut,
                g4_params=[[0.0001, 0.5, -1]],
            )
            feat_lst.append(acsf_ang.create(structure, centers=atomPos, n_jobs=4)[:,5:])
            # 15 x 2 = 30 features

        
        # combine the above functions (2d arrays) into one 2d array
        feat = np.hstack(tuple(feat_lst))

        np.savetxt(f'sym_{self.name}.csv', feat, delimiter=',')
        self.feat_atom['Ca'] = feat.flatten()

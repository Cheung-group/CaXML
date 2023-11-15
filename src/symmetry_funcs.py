import numpy as np
from ase.io import read
from dscribe.descriptors import ACSF


aN={1:'H',6:'C',7:'N',8:'O',20:'Ca'}

class Structure:
    
    def __init__(self, pdb_path):
        self.name = pdb_path.split('/')[1].split('.pdb')[0]
        self.water = int(self.name.split('.')[2][5:])
        self.system = self.name.split('.')[0]
        self.loop = self.name.split('.')[1]
        self.mdframe = self.name.split('.')[3]
        self.feat_atom=dict()
        #print("PDB name is ", self.name)
        
    def calc_sym(self):
        '''
        The function takes the structure file and compute the 
        symmetry function for each atom
        output: a list of symmetry functions for each atom. 
                Length of the list = number of atoms
            UPDATE: remove water molecules.
        ''' 
        pdb_file = self.name+'.pdb'
        chg_file = self.name + '.chg'
        structure = read("pdb/"+pdb_file)
        feat_lst=[]
        num=structure.get_global_number_of_atoms()
        atomPos = [x for x in range(0,num)]

        chg=np.genfromtxt("charge/"+chg_file)


        #for r_cut in [x/4. for x in range(4,13,1)]:
         
        # Setting up the ACSF descriptor
        for r_cut in [4.]:
            acsf = ACSF(
                species=["C", "H", "O", "N", "Ca"],
                rcut=r_cut,
                g2_params=[[0.0001,0]],
            )
            feat_lst.append(acsf.create(structure,positions=atomPos,n_jobs=4))

        acsf_ang = ACSF(
            species=["C", "H", "O", "N", "Ca"],
            rcut=6.0,
            g4_params=[[0.0001,0.5,-1]],
        )
        feat_lst.append(acsf_ang.create(structure,positions=atomPos,n_jobs=4))

        feat = np.hstack(tuple(feat_lst))
        dat = np.hstack((feat,chg))
        np.savetxt('sym/sym_'+pdb_file[0:-4]+'.dat', dat, delimiter=',')
        
        # Skip water here
        # Skip to the last water x 3 rows
        skip_water = -3 * self.water
        # If there is no water, skip none (-1)
        if skip_water == 0:
            skip_water = None
        #print("skip water atoms",skip_water)
        #print(dat.shape)
        #print(dat[:skip_water,:].shape)
        for i in dat[:skip_water,:]:
            ikey = aN[int(i[-2])]
            if ikey in self.feat_atom:
                self.feat_atom[ikey] = np.vstack((self.feat_atom[ikey],i))
            else:
                #print(ikey,"is not in the dictionary, adding ...")
                self.feat_atom[ikey] = i
# Main code to extract network parameters from pdb structures

import os
import argparse
from tqdm import tqdm
from pathlib import Path

import numpy as np
import pandas as pd

from Bio.PDB import PDBParser
from graph_feature_extraction import calc_dist_matrix, contact, network, sym_dist_matrix
from symmetry_funcs import Structure
from pymol import cmd

import warnings
from Bio import BiopythonWarning
warnings.simplefilter('ignore', BiopythonWarning)


parser = argparse.ArgumentParser(description='Extract network parameters from pdb structures')
parser.add_argument('dir', metavar='DIR', type=str, help='directory containing pdb files (pdb files with extension .pdb))')
args = parser.parse_args()


pdbdir = Path(args.dir)
allpdb = list(pdbdir.glob("*.pdb"))
count_total = len(allpdb)

# First convert pdb using pymol
def convert_pdb(infile, outfile):
    cmd.load(infile)
    cmd.sort()
    cmd.save(outfile)
    cmd.delete('all')

    
def get_network(network_file=None):
    net = pd.read_csv(network_file)
    return np.array(net.iloc[:, 1:]).flatten()


# Create network and extract network parameters
# deg_centrality = []
# bet_centrality = []
# close_centrality = []
# cluster_coeff = []

counter = 0

pdb_codes = []
feature_matrix = None

for struct in tqdm(allpdb, total=count_total):
    pdb_code = struct.stem
    pdb_codes.append(pdb_code)
    pymol_pdb_path = f'pymol_{pdb_code}.pdb'
    convert_pdb(struct, pymol_pdb_path)

    structure = PDBParser().get_structure(pdb_code, pymol_pdb_path)
    dist_matrix = calc_dist_matrix(structure, structure, method='heavy')

    dist = sym_dist_matrix(dist_matrix)
    edgefile = f'edgelist.{pdb_code}.csv'
    netparmfile = f'net.{pdb_code}.csv'
    
    contact(edgefile, dist, cutoff=7)
    (dc, bc, cce, cco) = network(edgefile,	netparmfile)
    # deg_centrality.append(dc)
    # bet_centrality.append(bc)
    # close_centrality.append(cce)
    # cluster_coeff.append(cco)

    #print(f"{pdb_code},{dc},{bc},{cce},{cco}")
    # calculate symmetry parameters
    st = Structure(pymol_pdb_path)
    st.calc_sym()  

    # adding the 13 x 4 = 52 network parameters to the beginning of the feat matrix
    net = get_network(netparmfile)
    sym = st.feat_atom['Ca'].copy()

    del st # delete the structure object to free up memory

    feat = np.hstack((net, sym))
	
    feature_matrix = np.vstack((feature_matrix, feat)) if feature_matrix is not None else feat

    # remove the temporary files
    os.remove(pymol_pdb_path)
    os.remove(edgefile)
    os.remove(netparmfile)
    os.remove(f'sym_pymol_{pdb_code}.csv')

    counter = counter + 1


np.savetxt("feature_matrix.csv", feature_matrix, delimiter=",")
np.savetxt("pdb_codes.csv", np.array(pdb_codes), delimiter=",", fmt='%s')

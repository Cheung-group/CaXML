# Main code to extract network parameters from pdb structures

import sys
import argparse
from tqdm import tqdm
from pathlib import Path

from Bio.PDB import PDBParser
from graph_feature_extraction import calc_dist_matrix, loop_dist_matrix, contact, network
from symmetry_funcs import Structure

import warnings
from Bio import BiopythonWarning
warnings.simplefilter('ignore', BiopythonWarning)


parser = argparse.ArgumentParser(description='Extract network parameters from pdb structures')
parser.add_argument('dir', metavar='DIR', type=str, help='directory containing pdb files (pdb files with extension .pdb))')
args = parser.parse_args()


pdbdir = Path(args.dir)
allpdb = list(pdbdir.glob("*.pdb"))
count_total = len(allpdb)


# Create network and extract network parameters
deg_centrality = []
bet_centrality = []
close_centrality = []
cluster_coeff = []

counter = 0
for struct in tqdm(allpdb, total=count_total):
    ###pdb_code = struct.split('/')[-1].split('.pdb')[0]
    pdb_code = struct.stem
    structure = PDBParser().get_structure(pdb_code, struct)
    dist_matrix = calc_dist_matrix(structure,structure, method='heavy')

    dist = loop_dist_matrix(dist_matrix)
    edgefile = 'edgelist.'+pdb_code+'.csv'
    netparmfile = 'net.'+pdb_code+'.csv'
    contact(edgefile, dist)
    (dc, bc, cce, cco) = network(edgefile,netparmfile)
    deg_centrality.append(dc)
    bet_centrality.append(bc)
    close_centrality.append(cce)
    cluster_coeff.append(cco)

    #print(f"{pdb_code},{dc},{bc},{cce},{cco}")
    counter = counter + 1
    #if counter % 100 == 0:
    #    print(counter, "structures processed ...", end = '\r')
    #    sys.stdout.flush()



# calculate symmetry parameters
# Use all the files
loops = allpdb

structures = dict()
counter = 0

for loop in tqdm(loops, total=count_total):
    #print(loop)
    #name = loop.split('/')[-1].split('.pdb')[0]
    name = loop.stem
    structures[name]=Structure(loop)
    structures[name].calc_sym()  

    counter = counter + 1
    # if counter % 100 == 0:
    #     #sys.stdout.write('\r')
    #     print(counter, "structures out of ", count_total, " processed ...", end = '\r')
    #     sys.stdout.flush()

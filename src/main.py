# Main code to extract network parameters from pdb structures

import glob
import sys
import argparse
from Bio.PDB import PDBParser
from .graph_feature_extraction import calc_dist_matrix, loop_dist_matrix, contact, network
from .symmetry_funcs import Structure

parser = argparse.ArgumentParser(description='Extract network parameters from pdb structures')
parser.add_argument('dir', metavar='DIR', type=str, help='directory containing pdb files')
args = parser.parse_args()

allpdb = glob.glob(args.dir + "/*.pdb")
deg_centrality = []
bet_centrality = []
close_centrality = []
cluster_coeff = []

counter = 0
for struct in allpdb:
    pdb_code = struct.split('/')[-1].split('.pdb')[0]
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

    print(f"{pdb_code},{dc},{bc},{cce},{cco}")
    counter = counter + 1
    if counter % 100 == 0:
        print(counter, "structures processed ...", end = '\r')
        sys.stdout.flush()



# Use all the files
loops = allpdb

structures = dict()
counter = 0
count_total = len(loops)
for loop in loops:
    name = loop.split('/')[1].split('.pdb')[0]
    structures[name]=Structure(loop)
    structures[name].calc_sym()  

    counter = counter + 1
    if counter % 100 == 0:
        #sys.stdout.write('\r')
        print(counter, "structures out of ", count_total, " processed ...", end = '\r')
        sys.stdout.flush()
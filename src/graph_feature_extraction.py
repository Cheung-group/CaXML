from Bio.PDB import *
import numpy as np
import csv
from operator import itemgetter
import networkx as nx

LARGE_DISTANCE = 99

def calc_residue_dist(residue_one, residue_two, method="heavy"):
    """Calculate the minimum distance between two residues.
    Parameters
    ----------
    residue_one, residue_two : Bio.PDB.Residue.Residue
    method : str, optional, default: "heavy"
        method to account for residual distance. Options are "heavy", "calpha", "oxygen-calcium", or "allatom", representing the heavy atoms, alpha carbons, oxygen and calcium atoms, and all atoms, respectively. Minimum distance between all selected atoms are returned as residual distance.

    Returns
    -------
    dist : float
    """
    dist_ij = []

    if method == 'allatom':
        for i in residue_one:
            for j in residue_two:
                r_ij = np.linalg.norm(i.coord - j.coord)
                dist_ij.append(r_ij)
    elif method == 'calpha':
        for i in residue_one:
            for j in residue_two:
                if i.id in ['CA', 'OW'] and j.id in ['CA', 'OW']:
                    r_ij = np.linalg.norm(i.coord - j.coord)
                    dist_ij.append(r_ij)
    elif method == 'oxygen-calcium':
        for i in residue_one:
            for j in residue_two:
                # Note here: more strict criteria for oxygen and calcium should be implemented. See biopython's PDB module for more details of atom id.
                if i.mass > 15 and j.mass > 15:
                    r_ij = np.linalg.norm(i.coord - j.coord)
                    dist_ij.append(r_ij)
    else:
        for i in residue_one:
            for j in residue_two:
                if i.mass > 12 and j.mass > 12:
                    r_ij = np.linalg.norm(i.coord - j.coord)
                    dist_ij.append(r_ij)

    # If there is no oxgyen (cap)
    # then return a large distance
    if not dist_ij:
        return LARGE_DISTANCE
    else:
        return min(dist_ij)


def calc_dist_matrix(chain_one, chain_two, method='oxygen-calcium'):
    """calculate a matrix of minimum residual distances between two chains"""
    n_rows = len([res for res in chain_one.get_residues()])
    n_cols = len([res for res in chain_two.get_residues()])

    answer = np.zeros((n_rows, n_cols), np.float)
    row = 0
    for residue_one in chain_one.get_residues():
        col = 0
        for residue_two in chain_two.get_residues():
            answer[row, col] = calc_residue_dist(residue_one, residue_two, method)
            col = col + 1
        row = row + 1
    return answer


def sym_dist_matrix(dist_matrix, capped=False):
    '''returns a symmetrical array'''
    mloop = loop_dist_matrix(dist_matrix) is capped else dist_matrix[:13, :13] 
    
    return mloop

def loop_dist_matrix(dist_matrix):
    '''returns a symmetrical array'''
    mloop = dist_matrix[1:13, 1:13]
    mloop_ca = dist_matrix[1:13, 14:15]

    # Compose the full distance matrix
    # The matrix should be 14 x 14

    mtot = np.zeros((14, 14), np.float)
    mtot[:12, :12] = mloop
    mtot[:12, 12:13] = mloop_ca
    mtot[12:13, :12] = np.transpose(mloop_ca)

    # If there is >= 1 water
    # find the water nearest to the calcium ion
    if len(dist_matrix) > 15:
        mwater_ca = dist_matrix[15:, 14:15]
        water_id = np.argmin(mwater_ca) + 15
        mloop_water = dist_matrix[1:13, water_id]
        mca_water = dist_matrix[14:15, water_id]

        mtot[:12, 13] = mloop_water
        mtot[13, :12] = np.transpose(mloop_water)

        mtot[12:13, 13] = mca_water
        mtot[13, 12:13] = np.transpose(mca_water)

    return mtot


def contact(filename, mtot, cutoff=6):
    """default cutoff is 6 angstroms if not provided."""
    msize = len(mtot)
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(('Source', 'Target', 'Type', 'Weight'))
        for i in range(msize):
            for j in range(i + 1, msize):
                if mtot[i, j] < cutoff:
                    writer.writerow((i, j, 'Undirected', 1 / mtot[i, j]))


def network(inputcsv, outputcsv):
    """
    Extracts graph features from a CSV file and writes them to another CSV file.

    Args:
        inputcsv (str): The path to the input CSV file.
        outputcsv (str): The path to the output CSV file.

    Returns:
        Tuple containing the degree centrality, betweenness centrality, closeness centrality, and clustering coefficient of the graph.
    """
    edgelist = dict()
    with open(inputcsv, 'r') as fh:
        ereader = csv.reader(fh)  # Read the csv

        # Retrieve the data (using Python list comprehension and list slicing to remove the header row)
        for j in [n for n in ereader][1:]:
            if j[0] not in edgelist:
                edgelist[j[0]] = {j[1]: {"weight": j[3]}}
            else:
                edgelist[j[0]][j[1]] = {"weight": j[3]}

    G = nx.Graph(edgelist)
    # In case some graphs are not complete
    #G.add_nodes_from([str(i) for i in range(14)])
    # print(nx.degree(G))
    deg_centrality = nx.degree_centrality(G)
    bet_centrality = nx.betweenness_centrality(G, normalized=True, endpoints=False)
    close_centrality = nx.closeness_centrality(G)
    cluster_coeff = nx.clustering(G)
    # sorted(cluster_coeff.items(), key=lambda x: int(x[0]), reverse=False)

    with open(outputcsv, 'w') as fout:
        csvwriter = csv.writer(fout)
        csvwriter.writerow(('node', 'degree_cent', 'bet_cent', 'clust_coeff', 'close_cent'))
        for i in range(G.number_of_nodes()):
            i = str(i)
            csvwriter.writerow((i, deg_centrality[i], bet_centrality[i], cluster_coeff[i], close_centrality[i]))
    return deg_centrality, bet_centrality, close_centrality, cluster_coeff



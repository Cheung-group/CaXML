#!/bin/bash

#module load vmd

# for gmx cluster
#module load gromacs/5.0.7
#gmx cluster -f equil.trr -s ref.pdb -method gromos  -clid -cl
#frame=($(grep frame clusters.pdb  | awk '{print int(($4*10)/1000)+1, ($4*10)%1000}'))

# for neuronet
# frame number in cluster.dat start from 0.
# cluster (starting from 0),
# part index (starting from 1),
# frame number (starting from 0)
# (0 2 39 ...)
Nclusters=`wc -l cluster.dat | awk '{print $1/2}'`
frame=($(cat cluster.dat | awk 'NR%2 == 0 {print NR/2-1, int($1/1000)+1, $1%1000}'))
echo "There are a total of $Nclusters clusters"

for N in $(seq 1 $Nclusters); do
    j=$((N*3-3))

    i=${frame[$j]}
    part=${frame[$((j+1))]}
    fr=${frame[$((j+2))]}

    echo "for $i th cluster: "
    echo "extracting frame $fr (start from 0) from part $part"
    vmd -dispdev text -gro ../npt-nopr-${part}.gro -trr ../npt-nopr-${part}.trr \
        -e extract_loop3_CA_H2O_from_frame.tcl -args $i $((fr+2))
done

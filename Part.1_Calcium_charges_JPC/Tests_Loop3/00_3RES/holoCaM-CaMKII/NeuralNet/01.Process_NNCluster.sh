#!/bin/bash

module purge
module load matlab/r2018b
module load VMD/1.9.4

NATOM=162

# STEP 0:
# generate data for nn clustering.
# in this case, o-ca distance & o-ca-o angles.
# output: vectors.dat
vmd -dispdev text ../equil.pdb -e o-ca-o.dist_angle.tcl
# formating vectors.dat


# STEP 1:
# normalizing the data (according to max value of each quantity)
rm -f filename.txt
/share/apps/matlab-r2017b/bin/matlab -nodisplay -nosplash < normCol.m
sed -i "s/\,/\ /g" filename.txt

# STEP 2:
# perform neural net clustering
# output: neuralcluster.dat cluster.dat
./neuralnetclusterglobal.pl filename.txt


# STEP 3:
# extract structures for each cluster
Nclusters=`wc -l cluster.dat | awk '{print $1/2}'`

j=1
k=2

for(( i=0; i<$Nclusters; i++)); do
	sed "$j,$k w tmp0" cluster.dat
	awk -f transpose.awk tmp0  > tmp

	Ndata=`wc -l tmp | awk '{print $1}'`

	mv tmp cluster$i.dat

	./numericalsort.pl cluster$i.dat $i ../equil.pdb $NATOM

	cp cluster.pdb cluster$i.pdb
	rm -f cluster.pdb
    rm -f tmp0


	j=$((j+2))
	k=$((k+2))
done

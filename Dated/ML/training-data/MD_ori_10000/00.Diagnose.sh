#!/bin/sh

MD="/home/pengzhi/data/calML/ML/training-data/MD_ori_10000/LOOP_STRUCTURES"
bak=`pwd -P`
cd $MD

for sys in `ls *.pdb`; do
	echo $sys
    vmd -dispdev text -pdb $sys -e $bak/diagnose.tcl > log
done


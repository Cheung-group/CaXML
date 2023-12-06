#!/bin/bash
## Usage: bash pp.bash

declare -A firstResInLoop

# Use a dictionary to store the first residue of each loop
firstResInLoop[loop1]=20
firstResInLoop[loop2]=56
firstResInLoop[loop3]=93
firstResInLoop[loop4]=129

loopSize=12
outdir=input_md_pdbs


counter=0
for i in `ls md_pdbs/*.pdb`; do 
	counter=$((counter+1))
	name=`basename $i`
	loop=`echo $i | cut -d'.' -f2`
	fr=${firstResInLoop[$loop]}
	outfile=$outdir/$name
	python ../../src/pp.py -i $i -o $outfile -s $loopSize -fr $fr

done 


#!/bin/bash

# add Hydrogens.
#source ~/.bashrc
conda activate pymol

dir=`pwd -P`

cd LOOP_STRUCTURES/
# here replacing them with numbers.
for i in `ls *.pdb`; do
    loop=`echo $i | cut -f 2 -d . | cut -c5`
    echo $i
    rm -f tem.pdb
    python $dir/addH.py -i $i -o tem.pdb -l $loop
    mv tem.pdb $i
done

echo "DONE!"

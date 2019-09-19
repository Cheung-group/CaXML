# !/bin/bash

# Generate single point calculation for Gaussian.


# i is file name for the picked loop structures.
    rm -rf xsedeInp/
    mkdir xsedeInp/
    for i in `ls *.pdb`; do
        i=`basename $i .pdb`
        echo working on model $i

        # convert pdb to the correct format
        # output New.xyz
        rm -f New.xyz
        perl reformat.pl ${i}.pdb

        # replace the xyz part in the inp file
        sed '10 r New.xyz' template.inp > ${i}.inp
        sed -i s/NNN/${i}/g ${i}.inp
        mv ${i}.inp xsedeInp/

        rm -f out${i}.pdb
        rm -f New.xyz
    done

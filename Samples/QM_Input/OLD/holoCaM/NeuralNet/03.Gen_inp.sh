# !/bin/bash


# Generate single point calculation for Gaussian.

# Read the first argument
rm -rf RES$1
mkdir RES$1

# i is file name for the picked loop structures.
for i in `ls [0-9]*.[0-9]*.pdb | cut -f 1-2 -d .`; do
    echo working on model $i

    # add H
    rm -f out${i}.pdb
    python mod$1.py -i ${i}.pdb -o out${i}.pdb

    # convert pdb to the correct format
    # output New.xyz
    rm -f New.xyz
    perl reformat.pl out${i}.pdb

    # replace the xyz part in the inp file
    sed '10 r New.xyz' template.inp > loop_3_model_${i}.inp
    sed -i s/holo_loop_3_model_5/holo_loop_3_model_${i}/g loop_3_model_${i}.inp
    sed -i s/holo5/holo${i}/g loop_3_model_${i}.inp
    mv loop_3_model_${i}.inp RES$1

    rm -f out${i}.pdb
    rm -f New.xyz
done

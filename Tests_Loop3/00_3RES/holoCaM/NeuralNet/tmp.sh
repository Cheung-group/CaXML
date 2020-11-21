# !/bin/bash


# Generate single point calculation for Gaussian.

# i is file name for the picked loop structures.
for i in `ls [0-9]*.[0-9]*.pdb | cut -f 1-2 -d .`; do
    echo working on model $i

    # add H
    rm -f out${i}.pdb
    python mod$1.py -i ${i}.pdb -o out${i}.pdb
done

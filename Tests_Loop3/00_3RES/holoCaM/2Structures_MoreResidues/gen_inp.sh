# !/bin/bash


# Generate single point calculation for Gaussian.

# Read the first argument
rm -rf RES$1
mkdir RES$1

for i in 5 6; do
    echo working on model $i

    # add H
    rm -f out${i}.pdb
    python mod$1.py -i ${i}.pdb -o out${i}.pdb

    # convert pdb to the correct format
    # output New.xyz
    rm -f New.xyz
    perl reformat.pl out${i}.pdb

    # replace the xyz part in the inp file
    sed '11 r New.xyz' template.inp > loop_3_model_${i}.inp
    sed -i s/holo_loop_3_model_5/holo_loop_3_model_${i}/g loop_3_model_${i}.inp
    sed -i s/holo5/holo${i}/g loop_3_model_${i}.inp
    mv loop_3_model_${i}.inp RES$1
done

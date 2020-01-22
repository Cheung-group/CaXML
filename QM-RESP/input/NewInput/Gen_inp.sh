# !/bin/bash

# Generate single point calculation for Gaussian.

declare -A Chg
Chg=( [loop1]=0 [loop2]=-2 [loop3]=0 [loop4]=-3)

declare -A Mul
Mul=( [loop1]=1 [loop2]=1 [loop3]=1 [loop4]=1)


#    rm -rf xsedeInp/
#    mkdir xsedeInp/
    for i in `ls Selected/loop3*.pdb`; do
        i=`basename $i .pdb`
        loop=`echo $i | cut -f 1 -d .`
        echo working on model $i

        # convert pdb to the correct format
        # output New.xyz
        rm -f New.xyz
        perl reformat.pl Selected/${i}.pdb

        # replace the xyz part in the inp file
        sed '10 r New.xyz' template.inp > ${i}.inp
        sed -i "s/NNN/${i}/g; s/CHG/${Chg[$loop]}/g; s/MUL/${Mul[$loop]}/g" ${i}.inp
        mv ${i}.inp xsedeInp/

        rm -f out${i}.pdb
        rm -f New.xyz
    done

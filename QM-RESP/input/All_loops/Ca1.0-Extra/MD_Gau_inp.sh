# !/bin/bash

# Generate single point calculation for Gaussian.

declare -A Chg
Chg=( [loop1]=0 [loop2]=-2 [loop3]=0 [loop4]=-3)

declare -A Mul
Mul=( [loop1]=1 [loop2]=1 [loop3]=1 [loop4]=1)


    rm -rf MDInp-Extra/
    mkdir  MDInp-Extra/

    for i in `ls sample/loop*.pdb`; do
        i=`basename $i .pdb`
        loop=`echo $i | cut -f 1 -d .`
        echo working on model $i

        # convert pdb to the correct format
        # output New.xyz
        rm -f New.xyz
        perl pdb2xyz.pl sample/${i}.pdb
        sed -i 1,2d New.xyz

        # replace the xyz part in the inp file
        sed '10 r New.xyz' template.inp > ${i}.inp
        sed -i "s/NNN/${i}/g; s/CHG/${Chg[$loop]}/g; s/MUL/${Mul[$loop]}/g" ${i}.inp
        mv ${i}.inp MDInp-Extra/

        rm -f out${i}.pdb
        rm -f New.xyz
    done

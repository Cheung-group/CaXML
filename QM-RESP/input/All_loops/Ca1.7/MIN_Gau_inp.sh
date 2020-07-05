# !/bin/bash

# Generate single point calculation for Gaussian.

declare -A Chg
Chg=( [loop1]=0 [loop2]=-2 [loop3]=0 [loop4]=-3)

declare -A Mul
Mul=( [loop1]=1 [loop2]=1 [loop3]=1 [loop4]=1)


    rm -rf MinInp/
    mkdir MinInp/
    for i in `ls Selected/loop*.pdb`; do
        i=`basename $i .pdb`
        loop=`echo $i | cut -f 1 -d .`
        echo working on model $i

        rm -f New.xyz
        rm -f Min.xyz
        perl pdb2xyz.pl Selected/${i}.pdb
        num=`cat New.xyz | wc -l`
        obminimize -n 100 -sd -ff uff New.xyz | tail -n $num > Min.xyz

        sed -i 1,2d Min.xyz
        # replace the xyz part in the inp file
        sed '10 r Min.xyz' template.inp > ${i}.inp
        sed -i "s/NNN/${i}/g; s/CHG/${Chg[$loop]}/g; s/MUL/${Mul[$loop]}/g" ${i}.inp
        mv ${i}.inp MinInp/

        rm -f New.xyz
        rm -f Min.xyz
    done

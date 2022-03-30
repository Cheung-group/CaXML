# !/bin/bash

# Generate single point calculation for Gaussian.

LOOPdir=../1.LOOP_Extraction_From_MD_Data/LOOP_STRUCTURES


declare -A Chg
Chg=( [loop1]=0 [loop2]=-2 [loop3]=0 [loop4]=-3)

declare -A Mul
Mul=( [loop1]=1 [loop2]=1 [loop3]=1 [loop4]=1)


    rm -rf MinInp/
    mkdir MinInp/
    for i in `ls $LOOPdir/*.pdb`; do
        i=`basename $i .pdb`
        loop=`echo $i | cut -f 2 -d .`
        echo working on model $i

        rm -f New.xyz
        rm -f Min.xyz
        perl pdb2xyz.pl $LOOPdir/${i}.pdb
        num=`cat New.xyz | wc -l`

        # Somehow the obminimize no longer works. 2/25/2021
        # obminimize -n 100 -sd -ff uff New.xyz | tail -n $num > Min.xyz
        obabel New.xyz -O Min.xyz --minimize --steps 500 --sd --ff UFF --crit 1e-4


        sed -i 1,2d Min.xyz
        # replace the xyz part in the inp file
        sed '10 r Min.xyz' template.inp > ${i}.inp
        sed -i "s/NNN/${i}/g; s/CHG/${Chg[$loop]}/g; s/MUL/${Mul[$loop]}/g" ${i}.inp
        mv ${i}.inp MinInp/

        rm -f New.xyz
        rm -f Min.xyz
    done

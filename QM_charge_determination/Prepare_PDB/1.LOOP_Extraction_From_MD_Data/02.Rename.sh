#!/bin/sh
# NAMING RULE
# SYS.LOOP.WATER.FRAME.pdb
# For NG, combine the three systems to add up the frames.
# 293 --> 1-500;
# 295 --> 501-1000;
# 31  --> 1001-1500

dir=`pwd -P`

rm -rf LOOP_STRUCTURES
mkdir LOOP_STRUCTURES


for sys in holoCaM holoCaM-CaMKII; do
    for loop in 1 2 3 4; do
	    cd $dir/$sys/loop$loop
        for i in `ls *.pdb`; do
            frame=`echo $i | cut -f 3 -d . | cut -c 6-`
            water=`echo $i | cut -f 4 -d . | cut -c 6-`
            new_name=${sys}.loop${loop}.water${water}.frame${frame}.pdb
            cp $i ${dir}/LOOP_STRUCTURES/${new_name}
            echo $new_name
        done
    done
done


sys=apoCaM-CA-Ng
for loop in 1 2 3 4; do
    j=0
    for traj in 293 295 31; do
        pre=$((j*500))
        #echo "For Ng, traj $traj, the frame prefix is $pre"
        cd $dir/$sys/loop$loop/$traj
        for i in `ls *.pdb`; do
            frame=`echo $i | cut -f 3 -d . | cut -c 6-`
            water=`echo $i | cut -f 4 -d . | cut -c 6-`
            frame=$((frame + pre))
            new_name=${sys}.loop${loop}.water${water}.frame${frame}.pdb
            echo $new_name
            cp $i ${dir}/LOOP_STRUCTURES/${new_name}
        done
        j=$((j+1))

	done
done

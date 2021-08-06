#!/bin/bash

dir=`pwd -P`


for atomic in 6 ; do
    rm -f $dir/nocap.i-RESP.c.dat
    rm -f $dir/nocap.i-RESP.c3.dat
    rm -f $dir/nocap.i-RESP.ca.dat

    for run in `cat $dir/cal.dat | awk '{print $1}'`; do
        if [ -f $run/fort.20.$run ]; then
           # echo -n $run >> $dir/$chgFile
           # delete the first two carbon and the last carbon
           grep ATOM $run/ANTECHAMBER_AC.AC | awk '{print $10}' > $run/type
           paste $run/fort.20.$run $run/type | awk '{if($1=='$atomic') print $0}' | sed 1,2d | head -n -1 > tem$run
           cat tem$run | awk '{if($3=="c") print $0}' >> $dir/nocap.i-RESP.c.dat
           cat tem$run | awk '{if($3=="c3") print $0}' >> $dir/nocap.i-RESP.c3.dat
           cat tem$run | awk '{if($3=="ca") print $0}' >> $dir/nocap.i-RESP.ca.dat
        fi
    done
done



for atomic in 7; do
    rm -f $dir/nocap.i-RESP.n.dat
    rm -f $dir/nocap.i-RESP.n4.dat

    for run in `cat $dir/cal.dat | awk '{print $1}'`; do
        if [ -f $run/fort.20.$run ]; then
           paste $run/fort.20.$run $run/type | awk '{if($1=='$atomic') print $0}' | head -n -1 > tem$run
           cat tem$run | awk '{if($3=="n") print $0}' >> $dir/nocap.i-RESP.n.dat
           cat tem$run | awk '{if($3=="n4") print $0}' >> $dir/nocap.i-RESP.n4.dat
        fi
    done
done


cd $dir
echo "Done"
exit

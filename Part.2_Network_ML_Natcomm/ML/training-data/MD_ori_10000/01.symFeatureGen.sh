#!/bin/sh

input="cal.iRESP_good.dat"
output="data.txt"
rm -f $output

while IFS= read -r line
do
    echo $line
    pdb=`echo $line | cut -f 1 -d " "`
    chg=`echo $line | cut -f 3 -d " "`
    feat=`python feat_sym.py LOOP_STRUCTURES/${pdb}.pdb`
    echo $feat $chg >> $output

done < "$input"


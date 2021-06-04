#!/bin/sh

input="i-RESP.$1.dat"
output="data.$1.txt"
rm -f $output

while IFS= read -r line
do
    echo $line
    pdb=`echo $line | cut -f 1 -d " "`
    chg=`echo $line | cut -f 3 -d " "`
    feat=`python feat_sym.py pdb/${pdb}.pdb`
    echo $feat $chg >> $output

done < "$input"


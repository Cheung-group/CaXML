#!/bin/sh

rm -f cn_com.txt

for i in `ls pdb/*.pdb`; do vmd -dispdev text -pdb $i -e cn_com.tcl | grep NNN | cut -c 4- >> cn_com.txt; done
for i in `ls pdb/*.pdb`; do i=`basename $i .pdb`; awk '$1 == 20 {print $2}' ../charge/$i.chg; done > ca.dat

paste cn_com.txt ca.dat > tem2
mv tem2 cn_com.txt

rm -f tem tem2 ca.dat

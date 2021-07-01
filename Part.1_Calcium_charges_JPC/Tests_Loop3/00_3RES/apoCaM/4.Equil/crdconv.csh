#!/bin/csh


echo 1 > ndx
cp ndx ndx2
cat ndx >> ndx2



gmx trjconv -s npt-nopr.tpr -f npt-nopr.trr -n index.ndx -pbc whole -o step1.xtc  < ndx
gmx trjconv -s npt-nopr.tpr -f step1.xtc -n index.ndx -pbc cluster -o step2.xtc < ndx2
gmx trjconv -s npt-nopr.tpr -f step2.xtc -n index.ndx -pbc nojump -o step3.xtc < ndx


#gmx trjconv -s npt-nopr.tpr -f npt-nopr.trr -n index.ndx -pbc mol -ur compact -o protein-ca.xtc < ndx
#gmx trjconv -s npt-nopr.tpr -f protein-ca.xtc -n index.ndx -center -o protein-ca-1.xtc < ndx2
#gmx trjconv -s npt-nopr.tpr -f protein-ca-1.xtc -n index.ndx -pbc nojump -o protein-ca-2.xtc < ndx


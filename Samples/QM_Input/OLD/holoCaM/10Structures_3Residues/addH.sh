#!/bin/bash

for i in {1..10}; do
    sed "s/\ CA\ \ CA\ /CA\ \ \ \ CA/g" $i.pdb > reform_$i.pdb
    babel -h -c reform_$i.pdb tem.pdb
    grep ATOM tem.pdb > loop_3.model_$i.pdb
    rm -f tem.pdb
done

for i in {1..0}; do
    /bin/cp loop_3.model_$i.pdb tem.pdb
    ./reseq.pl
    /bin/mv New.pdb toPiotr/loop_3.model_$i.pdb
    rm -f tem.pdb
done
